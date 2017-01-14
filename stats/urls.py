from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
    # host/stats/cli/
    url(r'^cli/$', views.cli, name='cli'),
]
