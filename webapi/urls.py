from django.conf.urls import url
from . import views

app_name = 'webapi'

urlpatterns = [
    # host/webapi/goal/crud/
    url(r'^goal/crud/$', views.crud, name='goal_crud'),
    # host/webapi/goal/read/regex/<GET PARAM>
    url(r'^goal/read/regex/$', views.read_regex, name='goal_read_regex'),
    # host/webapi/goal/read/family/pk
    url(r'^goal/read/family/(?P<pk>[1-9][0-9]*)/$', views.read_family, name='goal_read_family'),
]
