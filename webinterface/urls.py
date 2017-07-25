from django.conf.urls import url
from . import views

app_name = 'webinterface'

urlpatterns = [
    # host/goal/read/regex/?search=PATTERN
    url(r'^goal/read/regex/$', views.read_regex, name='goal_read_regex'),
    # host/goal/read/family/pk
    url(r'^goal/read/family/(?P<pk>[1-9][0-9]*)/$', views.read_family, name='goal_read_family'),
]
