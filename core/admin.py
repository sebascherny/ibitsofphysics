from django.contrib import admin
from .models import ContactMessage, SiteContent, Video

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key',)
    search_fields = ('key', 'content')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'vimeo_url', 'is_private')
    search_fields = ('title', 'vimeo_url')
