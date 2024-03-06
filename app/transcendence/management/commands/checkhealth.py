import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Check the health of the Django application'

    def handle(self, *args, **options):
        try:
            response = requests.get('http://localhost:8000/')
            response.raise_for_status()
            self.stdout.write(self.style.SUCCESS('Application is healthy'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Application is unhealthy: {e}'))
            raise SystemExit(1)

