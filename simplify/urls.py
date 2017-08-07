from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # Admin
    # host/admin/
    url(r'^admin/', admin.site.urls),

    # REST Api
    # host/rest/
    url(r'^rest/', include('restapi.urls')),

    # Web Interface
    # host/
    url(r'^', include('webinterface.urls')),
]
