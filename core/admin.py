from django.contrib import admin

from time_models import TimeTree, TimeBranch
from graph_models import Goal

admin.site.register(TimeTree)
admin.site.register(TimeBranch)
admin.site.register(Goal)
