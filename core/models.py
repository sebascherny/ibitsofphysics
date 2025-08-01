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


class Video(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=10, default='en')
    vimeo_url = models.URLField()
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({'Private' if self.is_private else 'Public'})"


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
    chapter = models.CharField(max_length=100)
    description = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='chapter_resources')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'order', 'chapter']
        unique_together = ('category', 'chapter')
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.chapter}"
