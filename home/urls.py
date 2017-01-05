from django.conf.urls import url, include

from . import views

app_name = 'home'

urlpatterns = [
    # host/
    url(r'^$', views.home, name='home'),
]
