from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    username = forms.CharField(required=False, help_text='Optional. If left empty, your email will be used.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # If username is empty, use email as username
        if not username and email:
            cleaned_data['username'] = email

        # Check if username (or email used as username) already exists
        if cleaned_data.get('username'):
            if User.objects.filter(username=cleaned_data['username']).exists():
                raise forms.ValidationError("A user with this username already exists.")

        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # If username was empty, use email
        if not self.cleaned_data.get("username"):
            user.username = self.cleaned_data["email"]
        
        if commit:
            user.save()
        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'autofocus': True}),
        help_text='Enter your username or email address.'
    )

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email is not None and password:
            # Try to authenticate with username first
            self.user_cache = authenticate(
                self.request, 
                username=username_or_email, 
                password=password
            )
            
            # If that fails and the input looks like an email, try to find user by email
            if self.user_cache is None and '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                    self.user_cache = authenticate(
                        self.request,
                        username=user.username,
                        password=password
                    )
                except User.DoesNotExist:
                    pass

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
