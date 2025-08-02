from django.db import models

class SiteContent(models.Model):
    key = models.CharField(max_length=100)
    language = models.CharField(max_length=10, default='en')
    content = models.TextField()

    class Meta:
        unique_together = ('key', 'language')

    def __str__(self):
        return f"{self.key} ({self.language})"

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
        ('notes_and_practice', 'Notes and practice'),
        ('notas_y_practica', 'Notas y práctica'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True, default="")
    language = models.CharField(max_length=10, default='en')
    chapter = models.CharField(max_length=100)
    description = models.TextField()
    vimeo_url = models.URLField(default="", blank=True, null=True)
    is_private = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'chapter']
        unique_together = ('category', 'chapter')
    
    def __str__(self):
        return f"{self.category}: {self.chapter}"
