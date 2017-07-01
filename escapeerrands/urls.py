from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    # host/admin/
    url(r'^admin/', admin.site.urls),

    # # host
    # url(r'^', ),
    # # host/errands/
    # url(r'^errands/', include("errands.urls")),
    # # host/time_table/
    # url(r'^time_table/', include("time_table.urls")),
    # # host/stats/
    # url(r'^cli/', include("cli.urls")),
]
