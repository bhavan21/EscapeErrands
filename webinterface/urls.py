from django.conf.urls import url
from . import views

app_name = 'webinterface'

urlpatterns = [
    # host/
    url(r'^$', views.home, name='home'),
    # host/goal/glance/
    url(r'^goal/glance/$', views.goal_glance, name='goal_glance'),
]
