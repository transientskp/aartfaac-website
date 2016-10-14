from pathlib import Path
from re import compile

from django.conf import settings


# used for matching with aartfaac images written in media folder
regex = compile("^S\d{3}_R01-63_T(.*)_corr.png$")


def image_list():
    """
    List all the images in he media root

    returns:
        list: of tuples with extracted date and full filename
    """
    p = Path(settings.MEDIA_ROOT)
    images = [f.name for f in p.glob('*.png')]
    matches = [regex.match(i) for i in images]
    dates = [(i.group(1), i.group(0)) for i in set(matches) if i]
    return dates
