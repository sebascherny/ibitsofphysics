from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from .models import ContactMessage
from .models import Video
from orders.views import has_user_with_email_paid

stripe.api_key = settings.STRIPE_SECRET_KEY

def home_view(request):
    return render(request, 'core/home.html')

def about_view(request):
    return render(request, 'core/about.html')

def miscellaneous_view(request):
    return render(request, 'core/miscellaneous.html')

def specimen_papers_view(request):
    return render(request, 'core/specimen_papers.html', {
        'videos': Video.objects.all(),
        'user_has_paid': request.user.profile.has_paid if request.user.is_authenticated else False
    })

def teacher_notes_view(request):
    return render(request, 'core/teacher_notes.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill out all fields.')
    return render(request, 'core/contact.html')

@login_required
def shop_view(request):
    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Private Videos Pack',
                    },
                    'unit_amount': 4000,  # $40.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=request.user.email,
            success_url=request.build_absolute_uri('/shop/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/shop/'),
            metadata={
                'user_id': request.user.id,
            }
        )
        return redirect(session.url, code=303)
    return render(request, 'core/shop.html', {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'has_paid': has_user_with_email_paid(request.user.email)
    })

def shop_success_view(request):
    return render(request, 'core/shop_success.html')
