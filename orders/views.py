from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem
import stripe
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = Decimal('0.00')
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            cart[product_id] = cart.get(product_id, 0) + 1
            request.session['cart'] = cart
            return redirect('cart')
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total)
        for product in products:
            quantity = cart[str(product.id)]
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        # Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # cents
            currency='usd',
            metadata={'order_id': order.id}
        )
        order.stripe_payment_intent = intent['id']
        order.save()
        request.session['order_id'] = order.id
        return render(request, 'orders/checkout.html', {
            'client_secret': intent['client_secret'],
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'order': order
        })
    return render(request, 'orders/checkout.html', {
        'client_secret': '',
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'order': None
    })

@login_required
def success_view(request):
    # Clear cart after successful payment
    request.session['cart'] = {}
    return render(request, 'orders/success.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return render(request, 'orders/webhook_error.html', {'error': str(e)})
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent['metadata'].get('order_id')
        user_id = intent['metadata'].get('user_id')
        # Update order if present
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'paid'
                order.save()
            except Order.DoesNotExist:
                pass
        # Update user profile for private video pack purchase
        if user_id:
            from accounts.models import UserProfile
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.has_paid = True
                if intent.get('customer'):
                    profile.stripe_customer_id = intent['customer']
                profile.save()
            except User.DoesNotExist:
                pass
    return render(request, 'orders/webhook_received.html')



def has_user_with_email_paid(email):
    has_more = True
    starting_after = None
    matched_customers = []

    while has_more:
        customers = stripe.Customer.list(limit=100, starting_after=starting_after)
        for customer in customers.data:
            if customer.email == email:
                matched_customers.append(customer)

        has_more = customers.has_more
        if has_more:
            starting_after = customers.data[-1].id

    return matched_customers