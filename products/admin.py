from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'product_type', 'is_active', 'created_at')
    list_filter = ('product_type', 'is_active')
    search_fields = ('name', 'description')
