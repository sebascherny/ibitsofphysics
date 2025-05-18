from django.db import models

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('digital', 'Digital'),
        ('physical', 'Physical'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default='digital')
    file = models.FileField(upload_to='products/files/', blank=True, null=True)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
