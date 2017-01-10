from django.conf.urls import url

from . import views

app_name = 'errands'

urlpatterns = [
    # host/errands/all/
    url(r'^all/$', views.all_, name='all'),
    # host/errands/touch/pk/
    url(r'^touch/(?P<pk>[0-9]+)/$', views.touch, name='touch'),
    # host/errands/process_touch/
    url(r'^process_touch/$', views.process_touch, name='process_touch'),
    # host/errands/delete/ -- pk is sent through POST method for security
    url(r'^delete/$', views.delete, name='delete'),

    # host/errands/fetch_errand/pk/
    url(r'^fetch_errand/(?P<pk>[0-9]+)/$', views.fetch_errand, name='fetch_errand'),
    # host/errands/fetch_piece/pk/
    url(r'^fetch_piece/(?P<pk>[0-9]+)/$', views.fetch_piece, name='fetch_piece'),
    # host/errands/fetch_stubs/
    url(r'^fetch_stubs/$', views.fetch_stubs, name='fetch_stubs'),
]
