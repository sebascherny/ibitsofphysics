from django import template
from django.utils.safestring import mark_safe
from core.models import SiteContent

register = template.Library()

import json

@register.simple_tag
def get_site_content_json(key, language='en'):
    try:
        content = SiteContent.objects.get(key=key, language=language).content
    except SiteContent.DoesNotExist:
        if language != 'en':
            try:
                content = SiteContent.objects.get(key=key, language='en').content
            except SiteContent.DoesNotExist:
                return []
        else:
            return []
    try:
        return json.loads(content)
    except Exception:
        return []

@register.simple_tag
def get_site_content(key, language='en'):
    try:
        content = SiteContent.objects.get(key=key, language=language).content
        # Convert newlines to HTML line breaks and mark as safe
        html_content = content.replace("\n", "<br/>")
        return mark_safe(html_content)
    except SiteContent.DoesNotExist:
        if language != 'en':
            try:
                content = SiteContent.objects.get(key=key, language='en').content
                html_content = content.replace("\n", "<br/>")
                return mark_safe(html_content)
            except SiteContent.DoesNotExist:
                return mark_safe('')
        return mark_safe('')
