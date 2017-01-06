from django.conf.urls import url, include

from . import views

app_name = 'home'

urlpatterns = [
    # host/
    url(r'^$', views.home, name='home'),
    # host/login/
    url(r'^login/$', views.login, name='login'),
    # host/logout/
    url(r'^logout/$', views.logout, name='logout'),
]
