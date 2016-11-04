import logging
from django.core.management.base import BaseCommand
from itertools import chain
from arthur.io import read_full
from django.conf import settings
import logging
from django.core.management.base import BaseCommand
from arthur.main import big_fat_loop_that_does_everything


class Command(BaseCommand):
    help = 'Listen on port for visibility stream'

    def add_arguments(self, parser):
        parser.add_argument('vis_file', nargs='+', type=str)
        parser.add_argument('--frequency', nargs=1, type=float,
                            default=58398437.5)

    def handle(self, *args, **options):
        logging.basicConfig()
        logger = logging.getLogger()
        if options['verbosity'] > 1:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        handler =logging.StreamHandler(self.stdout)
        handler.terminator = ""
        fmt = logging.Formatter(fmt="%(asctime)s -- %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)

        generator = chain(*map(read_full, options['vis_file']))
        big_fat_loop_that_does_everything(generator,  options['frequency'],
                                          settings.MEDIA_ROOT,
                                          settings.YOUTUBE_URL)
