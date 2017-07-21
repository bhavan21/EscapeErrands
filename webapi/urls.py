from django.conf.urls import url
from . import views

app_name = 'webapi'

urlpatterns = [
    # host/webapi/goal/gli/
    url(r'^goal/gli/$', views.GoalCRUD.list, name='goal_gli'),
]
