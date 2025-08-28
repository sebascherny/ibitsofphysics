from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import UserProfile, Code
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EmailOrUsernameAuthenticationForm
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            logger.info(f'User login successful: {user.username} (ID: {user.id}, Email: {user.email})')
            login(request, user)
            return redirect('profile')
        else:
            username_or_email = request.POST.get('username', 'unknown')
            logger.warning(f'Failed login attempt for username/email: {username_or_email}')
            messages.error(request, 'Invalid username/email or password.')
    else:
        form = EmailOrUsernameAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    user_info = f'{request.user.username} (ID: {request.user.id})' if request.user.is_authenticated else 'anonymous'
    logger.info(f'User logout: {user_info}')
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            code_value = (form.cleaned_data.get('code') or '').strip()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            error_msg = "The code doesn't exist or your school doesn't have more accounts to create. Reach out to request some more"

            if code_value:
                logger.info(f'Registration attempt with code: {code_value} for user: {username}, email: {email}')
                try:
                    with transaction.atomic():
                        code_obj = Code.objects.select_for_update().get(code=code_value)
                        if code_obj.remaining_accounts <= 0:
                            logger.warning(f'Code {code_value} has no remaining accounts for user: {username}')
                            form.add_error('code', error_msg)
                        else:
                            user = form.save()
                            UserProfile.objects.create(user=user, code=code_obj, has_paid=True)
                            code_obj.remaining_accounts -= 1
                            code_obj.save(update_fields=['remaining_accounts', 'updated_at'])
                            logger.info(f'User registered successfully with paid access: {user.username} (ID: {user.id}, Email: {user.email}, Code: {code_value})')
                            login(request, user)
                            return redirect('profile')
                except Code.DoesNotExist:
                    logger.warning(f'Invalid code used in registration: {code_value} for user: {username}')
                    form.add_error('code', error_msg)
            else:
                user = form.save()
                UserProfile.objects.create(user=user, has_paid=False)
                logger.info(f'User registered successfully with free access: {user.username} (ID: {user.id}, Email: {user.email})')
                login(request, user)
                return redirect('profile')
        else:
            username = request.POST.get('username', 'unknown')
            logger.warning(f'Registration form validation failed for user: {username}, errors: {form.errors}')
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request, language):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    logger.info(f'User accessed profile: {request.user.username} (ID: {request.user.id}, Language: {language}, Has Paid: {profile.has_paid})')
    return render(request, 'accounts/profile.html', {'profile': profile, 'language': language})
