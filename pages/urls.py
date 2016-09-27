from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

template_pages = [
    'start',
    'about',
    'live',
    'team',
    'jobs',
    'collab',
    'related',
    'contact',
    'publications',
]


def make_url(page):
    return url(r'^{}$'.format(page),
               TemplateView.as_view(template_name="pages/{}.html".format(page)),
               name=page)

urlpatterns = [make_url(i) for i in template_pages]
urlpatterns += [url(r'^$', RedirectView.as_view(pattern_name='start'))]
