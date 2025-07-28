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
