from django.conf.urls import url

from . import views

app_name = 'time_table'

urlpatterns = [
    # host/time_table/scrolling_stubs/
    url(r'^scrolling_stubs/$', views.scrolling_stubs, name='scrolling_stubs'),
    # host/time_table/verbose/
    url(r'^verbose/$', views.verbose, name='verbose'),
]
