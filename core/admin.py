from django.contrib import admin, messages
from django import forms
from django.db import models
from django.shortcuts import redirect
from django.urls import path, reverse
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
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
    list_display = ('key', 'language', 'content_first_part', 'updated_at')
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
    list_display = ('category', 'chapter', 'title', 'vimeo_url', 'language', 'is_private', 'order', 'updated_at')
    list_filter = ('category', 'language', 'is_private')
    search_fields = ('chapter', 'description', 'title', 'vimeo_url')
    ordering = ('category', 'order', 'chapter')

    change_list_template = 'admin/core/chapterresource/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'load-mock-resources/',
                self.admin_site.admin_view(self.load_mock_resources_view),
                name='core_chapterresource_load_mock',
            ),
        ]
        return custom_urls + urls

    def load_mock_resources_view(self, request):
        if not request.user.is_superuser:
            self.message_user(request, _('You do not have permission to run this action.'), level=messages.ERROR)
            return redirect(reverse('admin:core_chapterresource_changelist'))

        if request.method != 'POST':
            self.message_user(request, _('Invalid request method.'), level=messages.ERROR)
            return redirect(reverse('admin:core_chapterresource_changelist'))

        try:
            call_command('load_mock_chapter_resources', '--clear')
            self.message_user(request, _('Mock chapter resources loaded successfully.'), level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, _('Error loading mock resources: %s') % e, level=messages.ERROR)
        return redirect(reverse('admin:core_chapterresource_changelist'))
