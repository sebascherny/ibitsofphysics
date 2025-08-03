import json
import os
from django.core.management.base import BaseCommand, CommandError
from core.models import ChapterResource

class Command(BaseCommand):
    help = 'Load mock chapter resources and link them to existing videos.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing chapter resources before loading')

    def handle(self, *args, **options):
        if options['clear']:
            ChapterResource.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing chapter resources'))

        # Sample chapter resources data for each category
        created = 0
        for mock_file_name in [
            'mock_audiobook_hl_only.json',
            'mock_audiobook_sl_hl.json',
            'mock_audiolibro_nm_ns.json',
            'mock_audiolibro_ns_solo.json',
            'mock_notas_y_practica.json',
            'mock_notes_and_practice.json',
        ]:
            sample_data = json.load(open(os.path.join(os.path.dirname(__file__), "../../../mock_data", mock_file_name)))
            for chapter_data in sample_data:
                ChapterResource.objects.create(
                    category=chapter_data['category'],
                    chapter=chapter_data['chapter'],
                    description=chapter_data['description'],
                    vimeo_url=chapter_data['vimeo_url'],
                    is_private=chapter_data['is_private'],
                    order=chapter_data.get('order', 0)
                )
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created} chapter resources from 6 files.'
            )
        )
