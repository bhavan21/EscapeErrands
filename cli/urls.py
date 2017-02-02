from django.conf.urls import url

from . import views

app_name = 'cli'

urlpatterns = [
    # host/cli/
    url(r'^$', views.cli, name='cli'),
]
