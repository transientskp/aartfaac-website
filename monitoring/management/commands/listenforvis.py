import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from arthur.writer import create_all_images
from arthur.io import listen_socket


class Command(BaseCommand):
    help = 'Listen on port for visibility stream'

    def add_arguments(self, parser):
        parser.add_argument('--port', nargs=1, type=int, default=5000)

    def handle(self, *args, **options):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(self.stdout))
        create_all_images([listen_socket(options['port'])], settings.MEDIA_ROOT)
