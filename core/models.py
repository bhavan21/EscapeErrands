from __future__ import unicode_literals

import math
from django.db import models
from datetime import datetime as dt, timedelta as td

from core.classes import Stub
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
    time_period = models.DurationField(blank=True, null=True)
    duration = models.DurationField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_savable = self.is_savable()
        if is_savable is True:
            super(TimeBranch, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
            return True
        else:
            return is_savable

    def is_savable(self):
        is_timewise_valid = self.is_timewise_valid()
        if is_timewise_valid is True:
            is_standard = self.is_standard()
            if is_standard is True:
                return True
            else:
                error_message = is_standard[1]
        else:
            error_message = is_timewise_valid[1]

        return False, error_message

    def is_timewise_valid(self):
        # Duration
        if self.duration is None:
            return False, 'No duration'
        if not isinstance(self.duration, td):
            return False, 'Invalid duration'
        if self.duration <= td():
            return False, 'Non positive duration'

        # Time Period
        if self.time_period is not None:
            if not isinstance(self.time_period, td):
                return False, 'Invalid time period'
            if self.time_period <= td():
                return False, 'Non positive time period'
            if self.time_period <= self.duration:
                return False, 'time period <= duration'

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
        if self.time_period is not None:
            if self.time_period < TimeBranch.Standards.MIN_TPR:
                return False, 'Too small time period'
            if self.time_period > TimeBranch.Standards.MAX_TPR:
                return False, 'Too big time period'

        if self.duration < TimeBranch.Standards.MIN_DUR:
            return False, 'Too small duration'
        if self.duration > TimeBranch.Standards.MAX_DUR:
            return False, 'Too big duration'

        return True

    # todo : can return a better format of snapshot (than all the stubs)
    # Time complexity
    # if time_period, O(n) where n = window / time_period
    # else O(1)
    def get_snapshot(self, lp, up):
        if self.is_savable() is not True:
            return False
        if lp >= up:
            return False

        # Non Repeating
        if self.time_period is None:
            epoch = self.epoch
            end = self.end
            if end <= lp or epoch >= up:
                return []
            else:
                stub_epoch = max([lp, epoch])
                stub_end = min([end, up])
                stub_duration = stub_end - stub_epoch
                return [Stub(stub_epoch, stub_end, stub_duration)]
        # Repeating
        else:
            snapshot = []
            duration = self.duration
            time_period = self.time_period

            if self.epoch is None:
                init_end = self.end

                if init_end > up:
                    num = to_microseconds(init_end - up)
                    den = to_microseconds(time_period)
                    no_of_time_periods = int(math.floor(float(num) / float(den)))
                    i_end = init_end - (time_period * no_of_time_periods)
                    i_epoch = i_end - duration
                    if i_epoch < up:
                        stub_epoch = i_epoch
                        stub_end = min([i_end, up])
                        stub_duration = stub_end - stub_epoch
                        snapshot.append(Stub(stub_epoch, stub_end, stub_duration))
                    i_end -= time_period
                elif up >= init_end > lp:
                    i_end = init_end
                else:
                    return []

                loop_limit = lp

                while i_end > loop_limit:
                    i_epoch = i_end - duration
                    stub_epoch = max([i_epoch, loop_limit])
                    stub_end = i_end
                    stub_duration = stub_end - stub_epoch
                    snapshot.append(Stub(stub_epoch, stub_end, stub_duration))
                    i_end -= time_period
            else:
                init_epoch = self.epoch

                if init_epoch < lp:
                    num = to_microseconds(lp - init_epoch)
                    den = to_microseconds(time_period)
                    no_of_time_periods = int(math.floor(float(num) / float(den)))
                    i_epoch = init_epoch + (time_period * no_of_time_periods)
                    i_end = i_epoch + duration
                    if i_end > lp:
                        stub_epoch = lp
                        stub_end = min([i_end, up])
                        stub_duration = stub_end - stub_epoch
                        snapshot.append(Stub(stub_epoch, stub_end, stub_duration))
                    i_epoch += time_period
                elif lp <= init_epoch < up:
                    i_epoch = init_epoch
                else:
                    return []

                if self.end is None:
                    loop_limit = up
                else:
                    loop_limit = min([self.end, up])

                while i_epoch < loop_limit:
                    i_end = i_epoch + duration
                    stub_epoch = i_epoch
                    stub_end = min([i_end, loop_limit])
                    stub_duration = stub_end - stub_epoch
                    snapshot.append(Stub(stub_epoch, stub_end, stub_duration))
                    i_epoch += time_period

            return snapshot

    def __str__(self):
        return str(self.id)

    def __hash__(self):
        return hash((self.epoch, self.end, self.time_period, self.duration))

    def __eq__(self, other):
        if not isinstance(other, TimeBranch):
            return False
        return (self.epoch, self.end, self.time_period, self.duration) == (
            other.epoch, other.end, other.time_period, other.duration)

    def __ne__(self, other):
        return not self.__eq__(other)


class Goal(models.Model):
    # Relational fields
    id = models.AutoField(primary_key=True)
    __parents = models.ManyToManyField('Goal', related_name='__children')
    # Other fields
    description = models.TextField(default='')
    deadline = models.DateTimeField(blank=True, null=True)
    is_achieved = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_savable = self.is_savable()
        if is_savable is True:
            super(Goal, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
            return True
        else:
            return is_savable

    def is_savable(self):
        is_deadline_valid = self.is_deadline_valid()
        if is_deadline_valid is True:
            is_is_achieved_valid = self.is_is_achieved_valid()
            if is_is_achieved_valid is True:
                return True
            else:
                error_message = is_is_achieved_valid[1]
        else:
            error_message = is_deadline_valid[1]

        return False, error_message

    def is_deadline_valid(self):
        # Not saved yet
        if self.id is not None:
            for parent in self.__parents.all():
                if self.deadline is None and parent.deadline is None:
                    continue
                if self.deadline is None and parent.deadline is not None:
                    continue
                if self.deadline is not None and parent.deadline is None:
                    return False, 'Deadline before parent'
                if self.deadline is not None and parent.deadline is not None:
                    if self.deadline < parent.deadline:
                        return False, 'Deadline before parent'

            for child in self.__children.all():
                if self.deadline is None and child.deadline is None:
                    continue
                if self.deadline is None and child.deadline is not None:
                    return False, 'Deadline after child'
                if self.deadline is not None and child.deadline is None:
                    continue
                if self.deadline is not None and child.deadline is not None:
                    if self.deadline > child.deadline:
                        return False, 'Deadline after child'

            # No objection -> deadline valid
            return True
        else:
            return True

    def is_is_achieved_valid(self):
        if self.id is not None:
            if self.is_achieved is True:
                for parent in self.__parents.all():
                    if parent.is_achieved is False:
                        return False, 'This goal is achieved before its parent'
            elif self.is_achieved is False:
                for child in self.__children.all():
                    if child.is_achieved is True:
                        return False, 'Child goal is achieved before this'

            # No objection -> is_achieved valid
            return True
        else:
            return True

    def __dfs_for_checking_cycles(self, node, origin_id, at_root=True):
        if not at_root and node.id == origin_id:
            return True
        else:
            for child in node.__children.all():
                if self.__dfs_for_checking_cycles(child, origin_id, False) is True:
                    return True

    def is_acyclically_valid(self):
        # Assumes the graph before inserting this vertex is acyclic
        if self.id is not None:
            if self.__dfs_for_checking_cycles(self, self.id, True) is not True:
                return True
            else:
                return False, 'Forms cycle'
        else:
            return True

    def add_parents(self, parents_list):
        self.__parents.add(parents_list)
        is_acyclically_valid = self.is_acyclically_valid()
        if is_acyclically_valid is not True:
            self.__parents.remove(parents_list)
        return is_acyclically_valid

    def add_children(self, children_list):
        self.__children.add(children_list)
        is_acyclically_valid = self.is_acyclically_valid()
        if is_acyclically_valid is not True:
            self.__children.remove(children_list)
        return is_acyclically_valid

    def all_parents(self):
        return self.__parents.all()

    def all_children(self):
        return self.__children.all()

    def __str__(self):
        return str(self.id)
