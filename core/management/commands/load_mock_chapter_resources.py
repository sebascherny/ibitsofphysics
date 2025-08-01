import json
import os
from django.core.management.base import BaseCommand, CommandError
from core.models import ChapterResource, Video

class Command(BaseCommand):
    help = 'Load mock chapter resources and link them to existing videos.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing chapter resources before loading')

    def handle(self, *args, **options):
        if options['clear']:
            ChapterResource.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing chapter resources'))

        # Get available videos
        videos = list(Video.objects.all())
        if not videos:
            raise CommandError("No videos found. Please load videos first using 'python manage.py load_mock_videos'")

        # Sample chapter resources data for each category
        sample_data = {
            'audiobook_sl_hl': [
                {'chapter': 'Chapter 1: Measurements and Uncertainties', 'description': 'Introduction to physics measurements and error analysis'},
                {'chapter': 'Chapter 2: Mechanics', 'description': 'Kinematics and dynamics fundamentals'},
                {'chapter': 'Chapter 3: Thermal Physics', 'description': 'Temperature, heat, and thermodynamics'},
            ],
            'audiobook_hl_only': [
                {'chapter': 'Chapter 9: Wave Phenomena (HL)', 'description': 'Advanced wave concepts for Higher Level'},
                {'chapter': 'Chapter 10: Fields (HL)', 'description': 'Electric and magnetic fields in detail'},
                {'chapter': 'Chapter 11: Electromagnetic Induction (HL)', 'description': 'Faraday\'s law and applications'},
            ],
            'audiolibro_nm_ns': [
                {'chapter': 'Capítulo 1: Mediciones e Incertidumbres', 'description': 'Introducción a las mediciones físicas y análisis de errores'},
                {'chapter': 'Capítulo 2: Mecánica', 'description': 'Fundamentos de cinemática y dinámica'},
                {'chapter': 'Capítulo 3: Física Térmica', 'description': 'Temperatura, calor y termodinámica'},
            ],
            'audiolibro_ns_solo': [
                {'chapter': 'Capítulo 9: Fenómenos Ondulatorios (NS)', 'description': 'Conceptos avanzados de ondas para Nivel Superior'},
                {'chapter': 'Capítulo 10: Campos (NS)', 'description': 'Campos eléctricos y magnéticos en detalle'},
                {'chapter': 'Capítulo 11: Inducción Electromagnética (NS)', 'description': 'Ley de Faraday y aplicaciones'},
            ],
            'notes_and_practice': [
                {'chapter': 'Topic 1: Practice Problems', 'description': 'Comprehensive practice exercises for measurements'},
                {'chapter': 'Topic 2: Study Notes', 'description': 'Detailed notes and examples for mechanics'},
                {'chapter': 'Topic 3: Exam Preparation', 'description': 'Past paper questions and solutions'},
            ],
            'notas_y_practica': [
                {'chapter': 'Tema 1: Problemas de Práctica', 'description': 'Ejercicios completos para mediciones'},
                {'chapter': 'Tema 2: Notas de Estudio', 'description': 'Notas detalladas y ejemplos de mecánica'},
                {'chapter': 'Tema 3: Preparación de Examen', 'description': 'Preguntas de exámenes pasados y soluciones'},
            ],
        }

        created = 0
        video_index = 0

        for category, chapters in sample_data.items():
            for order, chapter_data in enumerate(chapters, 1):
                # Cycle through available videos
                video = videos[video_index % len(videos)]
                video_index += 1

                ChapterResource.objects.create(
                    category=category,
                    chapter=chapter_data['chapter'],
                    description=chapter_data['description'],
                    video=video,
                    order=order
                )
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created} chapter resources across {len(sample_data)} categories'
            )
        )
