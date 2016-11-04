import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from monitoring.images import image_list
from os import unlink, path

filename_template = "S{band}_R01-63_{timestamp}_{figure}.png"


class Command(BaseCommand):
    help = 'Delete old images, keep up to x number controlled by keep argument'

    def add_arguments(self, parser):
        parser.add_argument('--keep', nargs=1, type=int, default=1000)
        parser.add_argument('-y', '--yes', help="don't ask for confirmation",
                            action="store_true")

    def handle(self, *args, **options):
        keep = options['keep']
        yes = options['yes']
        images = sorted(image_list(), key=lambda x: x[0])
        deletes = [i[1] for i in images[:-keep]]

        if not yes and deletes:
            print("about to delete these files:\n")
            for delete in deletes:
                print("  * {}".format(delete))
            answer = input("\nDo you want to continue? [y/N] ")
            if answer.lower() != 'y':
                sys.stderr.write("Aborting.\n")
                sys.exit(1)
        for delete in deletes:
            print("deleting {}...".format(delete))
            unlink(path.join(settings.MEDIA_ROOT, delete))
