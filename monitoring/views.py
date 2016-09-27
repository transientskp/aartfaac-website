from pathlib import Path
from os import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from re import compile
from dateutil.parser import parse


def image_list():
    p = Path(path.join(settings.MEDIA_ROOT))
    return [f.name for f in p.glob('*.png')]


# used for matching with aartfaac images written in media folder
regex = compile("^S\d{3}_R01-63_T(.*)_corr.png$")


def dates():
    images = image_list()
    matches = [regex.match(i) for i in images]
    #dates = [parse(i.groups()[0]) for i in set(matches) if i]
    dates = [i.groups()[0] for i in set(matches) if i]
    return reversed(sorted(dates))


@method_decorator(login_required, name='dispatch')
class OverView(TemplateView):
    template_name = 'monitoring/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = image_list()
        return context


@method_decorator(login_required, name='dispatch')
class ListView(TemplateView):
    """
    Lists all available dates
    """
    template_name = 'monitoring/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = dates()
        return context


@method_decorator(login_required, name='dispatch')
class DateView(TemplateView):
    """
    Show images for a specific date
    """
    template_name = 'monitoring/date.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timestamp'] = self.kwargs['timestamp']
        return context
