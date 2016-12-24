from django.conf.urls import url

from . import views

app_name = 'time_table'

urlpatterns = [
    # host/time_table/
    url(r'^$', views.home, name='home'),
    # host/time_table/get_errands_on/
    url(r'^get_errands_on/$', views.get_errands_on, name='get_errands_on'),
]
