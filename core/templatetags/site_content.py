from django import template
from django.utils.safestring import mark_safe
from core.models import SiteContent, get_html_like_content

register = template.Library()


@register.simple_tag
def get_site_content(key, language='en'):
    try:
        html_content = get_html_like_content(None, key, language)
        # Convert newlines to HTML line breaks and mark as safe
        return mark_safe(html_content)
    except SiteContent.DoesNotExist:
        if language != 'en':
            try:
                html_content = get_html_like_content(None, key, 'en')
                return mark_safe(html_content)
            except SiteContent.DoesNotExist:
                return mark_safe('')
        return mark_safe('')
