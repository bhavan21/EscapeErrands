from django.conf.urls import url

from . import views

app_name = 'time_table'

urlpatterns = [
    # host/time_table/
    url(r'^$', views.home, name='home'),
]
