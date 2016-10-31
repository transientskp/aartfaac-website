import logging
from django.core.management.base import BaseCommand
from arthur.io import read_full
from arthur.writer import create_all_images
from django.conf import settings


class Command(BaseCommand):
    help = 'Open visibilities file and generate images in media store'

    def add_arguments(self, parser):
        parser.add_argument('vis_file', nargs='+', type=str)

    def handle(self, *args, **options):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(self.stdout))
        create_all_images(map(read_full, options['vis_file']),
                          settings.MEDIA_ROOT)
