from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    # Add more fields as needed, e.g. avatar, etc.

    def __str__(self):
        return f"{self.user.username} Profile"
