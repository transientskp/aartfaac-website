from django.conf.urls import url
from django.views.generic import RedirectView
from .views import OverView, ListView, DateView

urlpatterns = [
    url(r'^overview/$', OverView.as_view(), name='overview'),
    url(r'^list/$', ListView.as_view(), name='list'),
    url(r'^date/(?P<timestamp>\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2})$', DateView.as_view(), name='date'),
    url(r'^$', RedirectView.as_view(pattern_name='overview'))
]