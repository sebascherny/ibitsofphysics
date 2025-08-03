from django.contrib import admin
from django import forms
from django.db import models
from .models import ContactMessage, SiteContent, ChapterResource


class RichTextWidget(forms.Textarea):
    """Custom widget for rich text editing with formatting toolbar"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'vLargeTextField rich-text-editor',
            'rows': 15,
            'cols': 80,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    class Media:
        js = ('admin/js/rich_text_editor.js',)
        css = {
            'all': ('admin/css/rich_text_editor.css',)
        }


class SiteContentAdminForm(forms.ModelForm):
    """Custom form for ChapterResource with rich text editor"""
    
    content = forms.CharField(
        widget=RichTextWidget(),
        help_text="Use the rich text editor to format your description with bold, italic, lists, etc."
    )
    
    class Meta:
        model = SiteContent
        fields = '__all__'


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    form = SiteContentAdminForm
    list_display = ('key', 'language', 'content_first_part')
    search_fields = ('key', 'content')

    def content_first_part(self, obj):
        return (obj.content or '')[:200]
    content_first_part.description = "content"


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
