import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from arthur.writer import make_imaging_closure
from arthur.io import listen_socket
from arthur.imaging import full_calculation
from arthur.stream import setup_stream_pipe, stream
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Manager

logging.basicConfig()

logger = logging.getLogger(__name__)


def image_queue_pusher(date, body, frequency, queue):
    result = full_calculation(body, frequency)
    queue.put([date] + list(result))


def queue_repeater(in_queue, out_queues):
    logger.debug("repeater starting")
    while True:
        result = in_queue.get()
        logger.debug("Got something from repeat queue!")
        for queue in out_queues:
            queue.put(result)


def write_scheduler(queue, frequency):
    imager_writer = make_imaging_closure(settings.MEDIA_ROOT, frequency)
    while True:
        logger.debug("recieved on writer queue")
        result = queue.get()
        imager_writer(*result)


def stream_scheduler(queue):
    pipe = setup_stream_pipe(settings.YOUTUBE_URL)
    while True:
        _, img_data, _, _ = queue.get()
        logger.debug("Got something from stream queue!")
        stream(img_data, pipe)


class Command(BaseCommand):
    help = 'Listen on port for visibility stream'

    def add_arguments(self, parser):
        parser.add_argument('--port', nargs=1, type=int, default=5000)
        parser.add_argument('--frequency', nargs=1, type=float,
                            default=58398437.5)

    def handle(self, *args, **options):
        port = options['port']
        frequency = options['frequency']

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler =logging.StreamHandler(self.stdout)
        handler.terminator = ""
        fmt = logging.Formatter(fmt="%(asctime)s -- %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)

        manager = Manager()
        repeat_queue = manager.Queue()
        writer_queue = manager.Queue()
        stream_queue = manager.Queue()

        with ProcessPoolExecutor() as executor:
            executor.submit(queue_repeater, repeat_queue,
                            [writer_queue, stream_queue])
            executor.submit(write_scheduler, writer_queue, frequency)
            executor.submit(stream_scheduler, stream_queue)
            for date, body in listen_socket(port):
                executor.submit(image_queue_pusher, date, body,
                                frequency, repeat_queue)
