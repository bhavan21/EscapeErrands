from django.conf.urls import url
from . import views

app_name = 'webapi'

urlpatterns = [
    # host/webapi/timebranch/create/
    url(r'^timebranch/create/$', views.TimeBranchCRUD.create, name='timebranch_create'),

]
