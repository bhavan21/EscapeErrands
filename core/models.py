from __future__ import unicode_literals

from django.db import models
from datetime import datetime as dt, timedelta as td
from escapeerrands.timeutils import to_microseconds


class TimeTree(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)


class TimeBranch(models.Model):
    class Standards:
        MIN_TPR = td(0, 43200)
        MAX_TPR = td(740)
        MIN_DUR = td(0, 1800)
        MAX_DUR = td(15)

        def __init__(self):
            pass

    # Relational fields
    id = models.AutoField(primary_key=True)
    parent_tree = models.ForeignKey(TimeTree, on_delete=models.CASCADE)
    # Time fields
    epoch = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    time_period = models.DurationField()
    duration = models.DurationField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_valid = self.is_valid()
        if is_valid is True:
            is_standard = self.is_standard()
            if is_standard is True:
                super(TimeBranch, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
                return True
            else:
                error_message = is_standard[1]
        else:
            error_message = is_valid[1]
        return False, error_message

    def is_valid(self):
        # Related Errand
        try:
            if self.parent_tree is None:
                return False, 'No related parent_tree'
            if not isinstance(self.parent_tree, TimeTree):
                return False, 'Invalid related parent_tree'
        except Exception:
            return False, 'No related parent_tree'

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

    def is_standard(self):
        if self.time_period < TimeBranch.Standards.MIN_TPR:
            return False, 'Too small time period'
        if self.time_period > TimeBranch.Standards.MAX_TPR:
            return False, 'Too big time period'

        if self.duration < TimeBranch.Standards.MIN_DUR:
            return False, 'Too small duration'
        if self.duration > TimeBranch.Standards.MAX_DUR:
            return False, 'Too big duration'

        return True

    def __str__(self):
        return str(self.id)

    def __hash__(self):
        return hash((self.epoch, self.end, self.time_period, self.duration))

    def __eq__(self, other):
        return (self.epoch, self.end, self.time_period, self.duration) == (
            other.epoch, other.end, other.time_period, other.duration)
