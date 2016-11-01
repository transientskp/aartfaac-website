import logging
from django.core.management.base import BaseCommand
from itertools import chain
from arthur.io import read_full
from arthur.writer import create_all_images
from django.conf import settings


class Command(BaseCommand):
    help = 'Open visibilities file and generate images in media store'

    def add_arguments(self, parser):
        parser.add_argument('vis_file', nargs='+', type=str)
        parser.add_argument('--frequency', nargs=1, type=float, default=58398437.5)

    def handle(self, *args, **options):
        frequency = options['frequency']
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(self.stdout))
        list(create_all_images(chain(*map(read_full, options['vis_file'])),
                               settings.MEDIA_ROOT, frequency))
