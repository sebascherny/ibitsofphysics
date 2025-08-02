from rest_framework import serializers
from .models import ChapterResource

class ChapterResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterResource
        fields = ['id', 'category', 'chapter', 'title', 'vimeo_url', 'language', 'is_private', 'order']
