from os import path, symlink, unlink
from django.core.management.base import BaseCommand
from django.conf import settings
import numpy as np
from arthur.imaging import full_calculation, calculate_lag
from arthur.io import read_full
from arthur.plot import plot_image, plot_lag, plot_chan_power, plot_corr_mat, plot_diff
from arthur.constants import FRQ, NUM_CHAN, BAND_LABEL


filename_template = "S{band}_R01-63_{timestamp}_{figure}.png"


class Command(BaseCommand):
    help = 'Open visibilities file and generate images in static store'

    def add_arguments(self, parser):
        parser.add_argument('vis_file', nargs='+', type=str)

    def handle(self, *args, **options):
        # initialise historical structures
        lags = []
        prev_data = date = img_data = corr_data = diff_data = None
        chan_data = np.zeros((NUM_CHAN, 60), dtype=np.float32)

        for open_vis in map(read_full, options['vis_file']):
            for date, body in open_vis:
                img_data, corr_data, chan_row = full_calculation(body)
                lags += [calculate_lag(date).seconds]
                if prev_data is None:
                    prev_data = img_data

                    # update historical data
                chan_data = np.roll(chan_data, 1)
                chan_data[:, 0] = chan_row
                diff_data = img_data - prev_data
                prev_data = img_data

                figures = (
                    ('image', plot_image(date, img_data)),
                    ('lag', plot_lag(lags)),
                    ('chan', plot_chan_power(chan_data)),
                    ('corr', plot_corr_mat(corr_data, FRQ, date)),
                    ('diff', plot_diff(diff_data, FRQ, date)),
                )

                timestamp = date.strftime("T%d-%m-%Y-%H-%M-%S%Z")
                for name, figure in figures:
                    args = {'band': BAND_LABEL,
                            'timestamp': timestamp,
                            'figure': name}
                    filename = path.join(settings.MEDIA_ROOT,
                                         filename_template.format(**args))
                    figure.savefig(filename)  # pad_inches=0, bbox_inches='tight')

                    # symlink to latest version
                    link_target = path.join(settings.MEDIA_ROOT, name + '.png')
                    if path.islink(link_target):
                        unlink(link_target)
                    symlink(filename, link_target)


