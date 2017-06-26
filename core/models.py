from __future__ import unicode_literals

from django.db import models


class Errand(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=10)


class Piece(models.Model):
    id = models.AutoField(primary_key=True)

    epoch = models.DateTimeField()
    end = models.DateTimeField()
    time_period = models.DurationField()
    duration = models.DurationField()
    EVENT, TASK = range(2)
    type = models.PositiveSmallIntegerField()

    errand = models.ForeignKey(Errand, on_delete=models.CASCADE)
