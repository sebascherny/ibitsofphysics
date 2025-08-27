from django.contrib import admin
from .models import UserProfile, Code

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_customer_id')

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'school', 'total_accounts', 'remaining_accounts', 'who_paid', 'amount_paid', 'created_at', 'updated_at'
    )
    search_fields = ('code', 'school', 'who_paid')
    list_filter = ('school',)
    readonly_fields = ('created_at', 'updated_at')
