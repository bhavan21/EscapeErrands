from __future__ import unicode_literals

from django.db import models


class Errands(models.Model):
    info = models.TextField(blank=True)

    def __str__(self):
        return self.pk
