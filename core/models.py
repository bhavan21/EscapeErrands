from __future__ import unicode_literals

from django.db import models


class Errand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Piece(models.Model):
    id = models.AutoField(primary_key=True)
    # Time fields
    epoch = models.DateTimeField()
    end = models.DateTimeField()
    time_period = models.DurationField()
    duration = models.DurationField()
    # Type fields
    EVENT = 0
    TASK = 1
    TYPES = (
        (EVENT, 'event'),
        (TASK, 'task'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPES, default=EVENT)
    # Relational fields
    errand = models.ForeignKey(Errand, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
