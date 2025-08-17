from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import UserProfile, Code
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EmailOrUsernameAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username/email or password.')
    else:
        form = EmailOrUsernameAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            code_value = (form.cleaned_data.get('code') or '').strip()
            error_msg = "The code doesn't exist or your school doesn't have more accounts to create. Reach out to request some more"

            if code_value:
                try:
                    with transaction.atomic():
                        code_obj = Code.objects.select_for_update().get(code=code_value)
                        if code_obj.remaining_accounts <= 0:
                            form.add_error('code', error_msg)
                        else:
                            user = form.save()
                            UserProfile.objects.create(user=user, code=code_obj, has_paid=True)
                            code_obj.remaining_accounts -= 1
                            code_obj.save(update_fields=['remaining_accounts', 'updated_at'])
                            login(request, user)
                            return redirect('profile')
                except Code.DoesNotExist:
                    form.add_error('code', error_msg)
            else:
                user = form.save()
                UserProfile.objects.create(user=user, has_paid=False)
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    return render(request, 'accounts/profile.html', {'profile': profile})
