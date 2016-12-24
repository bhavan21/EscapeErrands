from django.conf.urls import url

from . import views

app_name = 'errands'

urlpatterns = [
    # host/errands/all/
    url(r'^all/$', views.all_, name='all'),
    # host/errands/touch/pk/
    url(r'^touch/(?P<pk>[0-9]+)/$', views.touch, name='touch'),
]
