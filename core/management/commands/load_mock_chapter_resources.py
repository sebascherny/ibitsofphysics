import json
import os
from django.core.management.base import BaseCommand, CommandError
from core.models import ChapterResource
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_drive_rows():
    """
    Reads a Google Spreadsheet and returns its data as a list of lists.
    """
    sheet_url = "https://docs.google.com/spreadsheets/d/1HeExbko4rIRmNlTRi9cloTgIQTNHov6vhGsO2ulQspI/edit?gid=0#gid=0"
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    public_json = {
        "type": "service_account",
        "project_id": "project-for-sso-395806",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "universe_domain": "googleapis.com"
    }
    public_json["private_key_id"] = os.getenv("private_key_id")
    public_json["private_key"] = os.getenv("private_key")
    public_json["client_email"] = os.getenv("client_email")
    public_json["client_id"] = os.getenv("client_id")
    public_json["client_x509_cert_url"] = os.getenv("client_x509_cert_url")
    with open("credentials.json", "w") as f:
        json.dump(public_json, f)
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()
    os.remove("credentials.json")
    return data


def load_from_drive():
    headers = []
    created = 0
    for row in get_drive_rows():
        if not any(row):
            continue
        if not headers:
            headers = row
            continue
        if headers:
            ChapterResource.objects.create(
                category=row[headers.index('category')],
                chapter=row[headers.index('chapter')],
                description=row[headers.index('description')],
                vimeo_url=row[headers.index('vimeo_url')],
                drive_url=row[headers.index('drive_url')],
                is_private=row[headers.index('is_private')].lower() in ('true', '1'),
                order=int(row[headers.index('order')]),
                language=row[headers.index('language')],
            )
            created += 1
    return created


def load_from_mock():
    created = 0
    for mock_file_name in [
        'mock_audiobook_hl_only.json',
        'mock_audiobook_sl_hl.json',
        'mock_audiolibro_nm_ns.json',
        'mock_audiolibro_ns_solo.json',
        'mock_notas.json',
        'mock_notes.json',
        'mock_practicas.json',
        'mock_practices.json',
    ]:
        sample_data = json.load(open(os.path.join(os.path.dirname(__file__), "../../../mock_data", mock_file_name)))
        for chapter_data in sample_data:
            ChapterResource.objects.create(
                category=chapter_data['category'],
                chapter=chapter_data['chapter'],
                description=chapter_data['description'],
                vimeo_url=chapter_data.get('vimeo_url', ''),
                drive_url=chapter_data.get('drive_url', ''),
                is_private=chapter_data['is_private'],
                order=chapter_data.get('order', 0)
            )
            created += 1
    return created


class Command(BaseCommand):
    help = 'Load mock chapter resources and link them to existing videos.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing chapter resources before loading')

    def handle(self, *args, **options):
        if options['clear']:
            ChapterResource.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all existing chapter resources'))

        created = load_from_drive()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created} chapter resources from 6 files.'
            )
        )
