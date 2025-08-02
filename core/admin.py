from django.contrib import admin
from .models import ContactMessage, SiteContent, ChapterResource

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key',)
    search_fields = ('key', 'content')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')


@admin.register(ChapterResource)
class ChapterResourceAdmin(admin.ModelAdmin):
    list_display = ('category', 'chapter', 'title', 'vimeo_url', 'language', 'is_private', 'order')
    list_filter = ('category', 'language', 'is_private')
    search_fields = ('chapter', 'description', 'title', 'vimeo_url')
    ordering = ('category', 'order', 'chapter')
