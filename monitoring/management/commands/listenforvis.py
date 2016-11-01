import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from arthur.writer import create_all_images
from arthur.io import listen_socket
from arthur.stream import setup_stream_pipe, stream


logging.basicConfig()


class Command(BaseCommand):
    help = 'Listen on port for visibility stream'

    def add_arguments(self, parser):
        parser.add_argument('--port', nargs=1, type=int, default=5000)
        parser.add_argument('--frequency', nargs=1, type=float, default=58398437.5)

    def handle(self, *args, **options):
        port = options['port']
        frequency = options['frequency']

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(self.stdout))

        pipe = setup_stream_pipe(settings.YOUTUBE_URL)

        images = create_all_images(listen_socket(port), settings.MEDIA_ROOT,
                                   frequency)
        stream(images, pipe)