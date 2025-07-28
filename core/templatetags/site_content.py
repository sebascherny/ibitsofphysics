from django import template
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
        return SiteContent.objects.get(key=key, language=language).content
    except SiteContent.DoesNotExist:
        if language != 'en':
            try:
                return SiteContent.objects.get(key=key, language='en').content
            except SiteContent.DoesNotExist:
                return ''
        return ''
