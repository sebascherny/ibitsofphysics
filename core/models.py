from django.db import models
from django.template.context_processors import csrf
import os

class SiteContent(models.Model):
    key = models.CharField(max_length=100)
    language = models.CharField(max_length=10, default='en')
    content = models.TextField()

    class Meta:
        unique_together = ('key', 'language')

    def __str__(self):
        return f"{self.key} ({self.language})"


def get_html_like_content(request, key, language):
    content = SiteContent.objects.get(key=key, language=language).content
    if request:
        prefix = request.build_absolute_uri('/')
    else:
        prefix = os.getenv('FRONTEND_URL')
    if not prefix.endswith('/'):
        prefix += '/'
    content = content.replace('__REDIRECT_TO_STRIPE_75_en__', f'{prefix}subscribe-1-year')
    content = content.replace('__REDIRECT_TO_STRIPE_100_en__', f'{prefix}subscribe-2-years')
    content = content.replace('__REDIRECT_TO_STRIPE_75_es__', f'{prefix}suscripcion-1-anio')
    content = content.replace('__REDIRECT_TO_STRIPE_100_es__', f'{prefix}suscripcion-2-anios')
    content = content.replace('__REDIRECT_TO_STRIPE_40_en__', f'{prefix}subscribe-early-access')
    content = content.replace('__REDIRECT_TO_STRIPE_40_es__', f'{prefix}suscripcion-promo')
    content = content.replace('__REDIRECT_TO_CONTACT_es__', f'{prefix}contacto')
    content = content.replace('__REDIRECT_TO_CONTACT_en__', f'{prefix}contact')
    content = content.replace('__REDIRECT_TO_SUSCRIPTION_es__', f'{prefix}suscripcion')
    content = content.replace('__REDIRECT_TO_SUSCRIPTION_en__', f'{prefix}subscription')
    if request:
        token = csrf(request)['csrf_token']
        content = content.replace('__CSRF_TOKEN__', f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">')
    content = content.replace("\n", "<br/>")
    return content


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"


class ChapterResource(models.Model):
    CATEGORY_CHOICES = [
        ('audiobook_sl_hl', 'Audiobook SL HL'),
        ('audiobook_hl_only', 'Audiobook HL only'),
        ('audiolibro_nm_ns', 'Audiolibro NM NS'),
        ('audiolibro_ns_solo', 'Audiolibro NS sólo'),
        ('notes', 'Notes'),
        ('notas', 'Notas'),
        ('practice', 'Practice'),
        ('practica', 'Practica'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True, default="")
    language = models.CharField(max_length=10, default='en')
    chapter = models.CharField(max_length=100)
    description = models.TextField()
    vimeo_url = models.URLField(default="", blank=True, null=True)
    drive_url = models.URLField(default="", blank=True, null=True)
    is_private = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'chapter']
        unique_together = ('category', 'chapter', 'description')
    
    def __str__(self):
        return f"{self.category}: {self.chapter}"
