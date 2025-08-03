from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from .models import ContactMessage, ChapterResource, SiteContent
from accounts.models import UserProfile
from orders.views import has_user_with_email_paid
from django.template.context_processors import csrf

stripe.api_key = settings.STRIPE_SECRET_KEY

def home_view(request):
    return render(request, 'core/home.html')

def miscellaneous_view(request):
    return render(request, 'core/miscellaneous.html')

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

def chapter_resource_view(request, category):
    """View to display chapter resources for a specific category with conditional access"""
    # Check user payment status
    has_paid = False
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            has_paid = user_profile.has_paid
        except UserProfile.DoesNotExist:
            has_paid = False
    
    # Get all chapter resources for this category
    chapters = ChapterResource.objects.filter(category=category)
    
    # Get the display name for the category
    category_display = dict(ChapterResource.CATEGORY_CHOICES).get(category, category)
    
    context = {
        'chapters': chapters,
        'category': category,
        'category_display': category_display,
        'has_paid': has_paid,
        'user_authenticated': request.user.is_authenticated,
    }
    
    return render(request, 'core/chapter_resources.html', context)

@login_required
def subscription_view(request):
    """View to display subscription content and handle Stripe payment"""
    # Get user profile or create if doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get subscription content
    try:
        subscription_content = SiteContent.objects.get(key='subscription', language='en').content
        subscription_content = subscription_content.replace('__REDIRECT_TO_STRIPE_1__', f'{request.build_absolute_uri("/subscribe-1-year/")}')
        subscription_content = subscription_content.replace('__REDIRECT_TO_STRIPE_2__', f'{request.build_absolute_uri("/subscribe-2-years/")}')
        token = csrf(request)['csrf_token']
        subscription_content = subscription_content.replace('__CSRF_TOKEN__', f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">')
    except SiteContent.DoesNotExist:
        subscription_content = "Subscription information not available."
    
    if request.method == 'POST':
        if user_profile.has_paid:
            messages.info(request, 'You already have an active subscription!')
            return redirect('subscription')
        
        try:
            # Create Stripe checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'IBits of Physics Subscription',
                            'description': 'Full access to all physics content and materials',
                        },
                        'unit_amount': 5000,  # $50.00 in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/subscription/success/'),
                cancel_url=request.build_absolute_uri('/subscription/'),
                client_reference_id=str(request.user.id),
            )
            return redirect(session.url)
        except Exception as e:
            messages.error(request, f'Payment processing error: {str(e)}')
            return redirect('subscription')
    
    context = {
        'subscription_content': subscription_content,
        'has_paid': user_profile.has_paid,
    }
    
    return render(request, 'core/subscription.html', context)


@login_required()
def redirect_to_stripe_1_year(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if user_profile.has_paid:
        messages.info(request, 'You already have an active subscription!')
        return redirect('/subscription/', context={'has_paid': True})
    
    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'IBits of Physics 1 Year Subscription',
                        'description': 'Full access to all physics content and materials',
                    },
                    'unit_amount': 7500,  # $75.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/subscription/success/'),
            cancel_url=request.build_absolute_uri('/subscription/'),
            client_reference_id=str(request.user.id),
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Payment processing error: {str(e)}')
        return redirect('subscription')


@login_required()
def redirect_to_stripe_2_years(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if user_profile.has_paid:
        messages.info(request, 'You already have an active subscription!')
        return redirect('/subscription/', context={'has_paid': True})
    
    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'IBits of Physics 2 Years Subscription',
                        'description': 'Full access to all physics content and materials',
                    },
                    'unit_amount': 10000,  # $100.00 in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/subscription/success/'),
            cancel_url=request.build_absolute_uri('/subscription/'),
            client_reference_id=str(request.user.id),
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Payment processing error: {str(e)}')
        return redirect('subscription')


@login_required
def subscription_success_view(request):
    """View to handle successful subscription payment"""
    # Get user profile and mark as paid
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.has_paid = True
    user_profile.save()
    
    messages.success(request, 'Subscription successful! You now have access to all content.')
    return render(request, 'core/subscription_success.html')
