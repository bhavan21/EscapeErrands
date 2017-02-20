from django.conf.urls import url

from . import views

app_name = 'errands'

urlpatterns = [
    # host/errands/all/errands/
    url(r'^all/errands/$', views.all_errands, name='all_errands'),
    # host/errands/touch/errand/pk/
    url(r'^touch/errand/(?P<pk>[0-9]+)/$', views.touch, name='touch_errand'),
    # host/errands/process_touch/errand/
    url(r'^process_touch/errand/$', views.process_touch, name='process_touch_errand'),
    # host/errands/delete/errand/ -- pk is sent through POST method for security
    url(r'^delete/errand/$', views.delete_errand, name='delete_errand'),
    # host/errands/read/errand/pk/
    url(r'^read/errand/(?P<pk>[0-9]+)/$', views.read_errand, name='read_errand'),

    # host/errands/read/piece/pk/
    url(r'^read/piece/(?P<pk>[0-9]+)/$', views.read_piece, name='read_piece'),

    # host/errands/read/stubs/
    url(r'^read/stubs/$', views.read_stubs, name='read_stubs'),
]
