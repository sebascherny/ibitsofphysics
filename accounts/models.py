from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator


class Code(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-A-Za-z0-9]+$', message='Code must be alphanumeric (dashes allowed).')],
        help_text="Alphanumeric code (you may include dashes).",
    )
    school = models.CharField(max_length=255)
    total_accounts = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    remaining_accounts = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    who_paid = models.EmailField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    invoice = models.FileField(upload_to='invoices/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.school}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    has_paid = models.BooleanField(default=False)  # Grants access to private videos
    must_change_password = models.BooleanField(default=False)  # Force password change on first login
    code = models.ForeignKey(Code, on_delete=models.SET_NULL, null=True, blank=True)
    # Add more fields as needed, e.g. avatar, etc.

    def __str__(self):
        return f"{self.user.username} Profile"