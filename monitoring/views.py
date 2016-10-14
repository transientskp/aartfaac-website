from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from monitoring.images import image_list


@method_decorator(login_required, name='dispatch')
class OverView(TemplateView):
    """
    Overview shows the latest images and refreshes them
    """
    template_name = 'monitoring/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ListView(TemplateView):
    """
    Lists all available dates
    """
    template_name = 'monitoring/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = reversed(sorted(i[0] for i in image_list()))
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
