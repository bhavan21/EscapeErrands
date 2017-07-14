from django.contrib import admin

from models.timetree import TimeTree
from models.timebranch import TimeBranch
from core.models.goal import Goal
from models.job import Job

admin.site.register(TimeTree)
admin.site.register(TimeBranch)
admin.site.register(Goal)
admin.site.register(Job)
