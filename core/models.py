from __future__ import unicode_literals

from django.db import models
from datetime import datetime as dt, timedelta as td
from escapeerrands_dj.timeutils import to_microseconds


class Errand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id) + self.name


class Piece(models.Model):
    id = models.AutoField(primary_key=True)
    # Time fields
    epoch = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    time_period = models.DurationField()
    duration = models.DurationField()
    # Type fields
    TYPES_COUNT = 2
    EVENT, TASK = range(TYPES_COUNT)
    TYPES = (
        (EVENT, 'event'),
        (TASK, 'task'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPES)
    # Relational fields
    errand = models.ForeignKey(Errand, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_valid = self.is_valid()
        if is_valid is True:
            super(Piece, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return is_valid

    def is_valid(self):
        # Errand
        try:
            if self.errand is None:
                return False, 'No related errand'
            if not isinstance(self.errand, Errand):
                return False, 'Invalid related errand'
        except Exception:
            return False, 'No related errand'

        # Type
        if self.type is None:
            return False, 'No type'
        if not isinstance(self.type, int):
            return False, 'Invalid Type'
        if self.type >= Piece.TYPES_COUNT:
            return False, 'Invalid Type'

        # Time Period
        if self.time_period is None:
            return False, 'No time period'
        if not isinstance(self.time_period, td):
            return False, 'Invalid time period'
        if self.time_period <= td():
            return False, 'Non positive time period'

        # Duration
        if self.duration is None:
            return False, 'No duration'
        if not isinstance(self.duration, td):
            return False, 'Invalid duration'
        if self.duration <= td():
            return False, 'Non positive duration'

        # Epoch and End
        if self.epoch is None and self.end is None:
            return False, 'No epoch or end'
        elif self.epoch is not None and self.end is None:
            if not isinstance(self.epoch, dt):
                return False, 'Invalid epoch'
            if self.time_period is None:
                self.end = self.epoch + self.duration
        elif self.epoch is None and self.end is not None:
            if not isinstance(self.end, dt):
                return False, 'Invalid end'
            if self.time_period is None:
                self.epoch = self.end - self.duration
        elif self.epoch is not None and self.end is not None:
            if not isinstance(self.epoch, dt):
                return False, 'Invalid epoch'
            if not isinstance(self.end, dt):
                return False, 'Invalid end'
            if self.time_period is None:
                if self.epoch + self.duration != self.end:
                    return False, 'epoch + duration != end'
            else:
                last_epoch = self.end - self.duration
                num = to_microseconds(last_epoch - self.epoch)
                den = to_microseconds(self.time_period)
                if num < 0:
                    return False, 'Number of cycles < 0'
                elif num == 0:
                    self.time_period = None
                else:
                    no_cycles = float(num) / float(den)
                    if not no_cycles.is_integer():
                        return False, 'Non integral number of cycles'

        # No objection -> valid
        return True

    def __str__(self):
        return str(self.id)
