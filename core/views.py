from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe
from .models import ContactMessage, ChapterResource, SiteContent, get_html_like_content
from accounts.models import UserProfile
from orders.views import has_user_with_email_paid
from django.urls import reverse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def home_view(request):
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    logger.info(f'Home page accessed by user: {user_info}')
    return render(request, 'core/home.html')

def miscellaneous_view(request):
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    logger.info(f'Miscellaneous page accessed by user: {user_info}')
    return render(request, 'core/miscellaneous.html')

def teacher_notes_view(request):
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    logger.info(f'Teacher notes page accessed by user: {user_info}')
    return render(request, 'core/teacher_notes.html')

def contact_view(request, language):
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    logger.info(f'Contact page accessed by user: {user_info}, language: {language}')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        logger.info(f'Contact form submission: Name: {name}, Email: {email}, User: {user_info}, Language: {language}')
        
        # Server-side validation
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')
        if not message:
            errors.append('Message is required.')
        
        if errors:
            return render(request, 'core/contact.html', {
                'language': language,
                'name': name,
                'email': email,
                'message': message
            })
        
        try:
            contact_message = ContactMessage.objects.create(name=name, email=email, message=message)
            logger.info(f'Contact message saved successfully: ID {contact_message.id}, from {name} <{email}>')
            
            # Send email notification
            try:
                subject = f'New Contact Message from {name}'
                email_message = f"""
New contact message received:

Name: {name}
Email: {email}
Message:
{message}

Submitted at: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                send_mail(
                    subject=subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                logger.info(f'Email notification sent for contact message from {name} <{email}>')
            except Exception as email_error:
                logger.error(f'Failed to send email notification for contact message: {email_error}')
                # Continue with the redirect even if email fails
            
            return redirect(reverse('contact' if language == "en" else "contacto"))
        except Exception as e:
            logger.error(f'Error saving contact message: {e}')
            return render(request, 'core/contact.html', {
                'language': language,
                'name': name,
                'email': email,
                'message': message,
                'error': 'Error saving contact message' if language == "en" else 'Hubo un error enviando el mensaje, reintenta o envía un email directamente a ibitsofphysics@gmail.com'
            })
    
    return render(request, 'core/contact.html', {'language': language})

@login_required
def shop_view(request):
    logger.info(f'Shop page accessed by user: {request.user.username} (ID: {request.user.id})')
    
    if request.method == 'POST':
        try:
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
            logger.info(f'Stripe checkout session created for user {request.user.username}: Session ID {session.id}, Amount: $40.00')
            return redirect(session.url, code=303)
        except Exception as e:
            logger.error(f'Error creating Stripe checkout session for user {request.user.username}: {str(e)}', exc_info=True)
            return redirect('shop')
    
    return render(request, 'core/shop.html', {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'has_paid': has_user_with_email_paid(request.user.email)
    })

def shop_success_view(request):
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    session_id = request.GET.get('session_id', 'unknown')
    logger.info(f'Shop success page accessed by user: {user_info}, Session ID: {session_id}')
    return render(request, 'core/shop_success.html')

def chapter_resource_view(request, category, language="en"):
    """View to display chapter resources for a specific category with conditional access"""
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    
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
    
    logger.info(f'Chapter resources accessed: Category {category} ({category_display}) by user {user_info}, Language: {language}, Has Paid: {has_paid}, Resources Count: {chapters.count()}')
    
    context = {
        'chapters': chapters,
        'category': category,
        'category_display': category_display,
        'has_paid': has_paid,
        'user_authenticated': request.user.is_authenticated,
        'language': language,
    }
    
    return render(request, 'core/chapter_resources.html', context)


@require_http_methods(["GET"])
def subscription_view(request, language):
    """View to display subscription content and handle Stripe payment"""
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    
    # Get user profile or create if doesn't exist
    if not request.user.is_authenticated:
        has_paid = False
    else:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        has_paid = user_profile.has_paid
    
    logger.info(f'Subscription page accessed by user: {user_info}, Language: {language}, Has Paid: {has_paid}')
    
    # Get subscription content
    try:
        subscription_content = get_html_like_content(request, 'subscription', language)
    except SiteContent.DoesNotExist:
        subscription_content = "Subscription information not available."

    context = {
        'subscription_content': subscription_content,
        'has_paid': has_paid,
        'language': language,
    }
    
    return render(request, 'core/subscription.html', context)


@login_required()
@require_http_methods(["GET"])
def redirect_to_stripe(request, language, type):
    logger.info(f'Stripe redirect initiated by user: {request.user.username} (ID: {request.user.id}), Language: {language}, Type: {type}')
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if user_profile.has_paid:
        logger.info(f'User {request.user.username} already has paid subscription, redirecting to subscription page')
        messages.info(request, 'You already have an active subscription!')
        return redirect(
            reverse('subscription' if language == 'en' else 'suscripcion'),
            context={'has_paid': True, 'language': language}
        )
    
    if type == '1 year':
        unit_amount = 6000  # $60.00 in cents
        if language == 'es':
            name = 'IBits of Physics 1 Año'
            description = 'Acceso a todo el contenido'
        else:
            name = 'IBits of Physics 1 Year Subscription'
            description = 'Full access to all physics content and materials'
    elif type == '2 years':
        unit_amount = 9000  # $90.00 in cents
        if language == 'es':
            name = 'IBits of Physics 2 Años'
            description = 'Acceso a todo el contenido'
        else:
            name = 'IBits of Physics 2 Years Subscription'
            description = 'Full access to all physics content and materials'
    elif type == 'early access':
        unit_amount = 4000  # $40.00 in cents
        if language == 'es':
            name = 'IBits of Physics Acceso Temprano'
            description = 'Acceso temprano al contenido'
        else:
            name = 'IBits of Physics Early Access'
            description = 'Early access to all physics content and materials'
    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': name,
                        'description': description,
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('subscription_success_' + language)),
            cancel_url=request.build_absolute_uri(reverse('subscription' if language == 'en' else 'suscripcion')),
            client_reference_id=str(request.user.id),
        )
        logger.info(f'Stripe subscription checkout session created: User {request.user.username}, Type: {type}, Amount: ${unit_amount/100}, Session ID: {session.id}')
        return redirect(session.url)
    except Exception as e:
        logger.error(f'Error creating Stripe subscription session for user {request.user.username}: {str(e)}', exc_info=True)
        if language == 'es':
            messages.error(request, f'Error al procesar el pago: {str(e)}')
        else:
            messages.error(request, f'Payment processing error: {str(e)}')
        return redirect(
            reverse('error-in-payment' if language == 'en' else 'error-en-pago'),
            context={'has_paid': False, 'language': language}
        )


@login_required
def subscription_success_view(request, language):
    """View to handle successful subscription payment"""
    # Get user profile and mark as paid
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.has_paid = True
    user_profile.save()
    
    logger.info(f'Subscription success: User {request.user.username} (ID: {request.user.id}) marked as paid, Language: {language}')

    subscription_success_content = get_html_like_content(request, 'subscription_success', language)
    
    return render(request, 'core/subscription_success.html', {'language': language, 'subscription_success_content': subscription_success_content})


@login_required
def error_in_payment_view(request, language):
    logger.warning(f'Payment error page accessed by user: {request.user.username} (ID: {request.user.id}), Language: {language}')
    return render(request, 'core/error_in_payment.html', {'language': language})
