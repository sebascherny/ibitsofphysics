import json
import os
from django.core.management.base import BaseCommand
from core.models import SiteContent

class Command(BaseCommand):
    help = 'Load mock site content from mock_site_content.json into the SiteContent model.'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        json_path = os.path.join(base_dir, 'mock_data/mock_site_content.json')
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f'File not found: {json_path}'))
            return
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for lang, entries in data.items():
            for key, content in entries.items():
                if os.path.exists(os.path.join(base_dir, 'mock_data', f'{key}_{lang}.html')):
                    with open(os.path.join(base_dir, 'mock_data', f'{key}_{lang}.html'), 'r', encoding='utf-8') as f:
                        html_content = f.read()
                else:
                    html_content = content
                obj, created = SiteContent.objects.update_or_create(
                    key=key, language=lang,
                    defaults={'content': html_content}
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} items into SiteContent.'))
