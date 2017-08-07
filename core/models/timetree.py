from __future__ import unicode_literals

from django.db import models


class TimeTree(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)
