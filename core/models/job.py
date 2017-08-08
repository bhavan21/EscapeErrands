from __future__ import unicode_literals

from django.db import models
from timetree import TimeTree
from goal import Goal


class Job(models.Model):
    # Relational fields
    id = models.AutoField(primary_key=True)
    time_tree = models.OneToOneField(TimeTree, blank=True, null=True, on_delete=models.SET_NULL)
    _goals = models.ManyToManyField(Goal, related_name='_jobs')
    # Other fields
    description = models.TextField(default='')
    is_done = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_valid = self.is_valid()
        if is_valid is True:
            super(Job, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
            return True
        else:
            return is_valid

    def is_valid(self):
        is_is_done_valid = self.is_is_done_valid()
        if is_is_done_valid is True:
            is_timewise_valid = self.is_timewise_valid()
            if is_timewise_valid is True:
                return True
            else:
                error_message = is_timewise_valid[1]
        else:
            error_message = is_is_done_valid[1]

        return False, error_message

    def is_is_done_valid(self):
        if self.id is not None:
            if self.is_done is False:
                for goal in self._goals.all():
                    if goal.is_achieved is True:
                        return False, 'Goal is achieved before its job is done'

            # No objection -> is_achieved valid
            return True
        else:
            return True

    def is_timewise_valid(self):
        # Not saved yet
        if self.id is not None:
            if self.time_tree is not None and self._goals.count() > 0:
                for goal in self._goals.all():
                    for time_branch in self.time_tree.branches.all():
                        time_branch_end = time_branch.end
                        goal_end = goal.end
                        # goal_end must be >= time_branch_end
                        if time_branch_end is None and goal_end is None:
                            continue
                        elif time_branch_end is not None and goal_end is None:
                            continue
                        elif time_branch_end is None and goal_end is not None:
                            return False, 'Goal is achieved before its job finishes'
                        else:
                            if goal_end < time_branch_end:
                                return False, 'Goal is achieved before its job finishes'

            # No objection -> timewise valid
            return True
        else:
            return True

    def get_goals(self):
        return self._goals.all()

    def add_goal(self, goal):
        self._goals.add(goal)
        is_valid = self.is_valid()
        if is_valid is not True:
            self._goals.remove(goal)
        return is_valid

    def remove_goal(self, goal):
        self._goals.remove(goal)

    def __str__(self):
        return str(self.id)
