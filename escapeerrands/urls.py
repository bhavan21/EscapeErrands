from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # Admin
    # host/admin/
    url(r'^admin/', admin.site.urls),

    # Web Interface
    # host/
    url(r'^', include('webinterface.urls')),
]
