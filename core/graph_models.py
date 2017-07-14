from __future__ import unicode_literals

from django.db import models
from time_models import TimeTree


class Goal(models.Model):
    # Relational fields
    id = models.AutoField(primary_key=True)
    _parents = models.ManyToManyField('Goal', related_name='_children')
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
            for parent in self._parents.all():
                if self.deadline is None and parent.deadline is None:
                    continue
                if self.deadline is None and parent.deadline is not None:
                    continue
                if self.deadline is not None and parent.deadline is None:
                    return False, 'Deadline before parent'
                if self.deadline is not None and parent.deadline is not None:
                    if self.deadline < parent.deadline:
                        return False, 'Deadline before parent'

            for child in self._children.all():
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
                for parent in self._parents.all():
                    if parent.is_achieved is False:
                        return False, 'This goal is achieved before its parent'
            elif self.is_achieved is False:
                for child in self._children.all():
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
            for child in node.get_children().all():
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

    def get_parents(self):
        return self._parents.all()

    def add_parents(self, parents_list):
        self._parents.add(parents_list)
        is_acyclically_valid = self.is_acyclically_valid()
        if is_acyclically_valid is not True:
            self._parents.remove(parents_list)
        return is_acyclically_valid

    def remove_parents(self, parents_list):
        self._parents.remove(parents_list)

    def get_children(self):
        return self._children.all()

    def add_children(self, children_list):
        self._children.add(children_list)
        is_acyclically_valid = self.is_acyclically_valid()
        if is_acyclically_valid is not True:
            self._children.remove(children_list)
        return is_acyclically_valid

    def remove_children(self, children_list):
        self._children.remove(children_list)

    def get_jobs(self):
        return self._jobs.all()

    def add_jobs(self, jobs_list):
        self._jobs.add(jobs_list)

    def remove_jobs(self, jobs_list):
        self._jobs.remove(jobs_list)

    def __str__(self):
        return str(self.id)


class Job(models.Model):
    # Relational fields
    id = models.AutoField(primary_key=True)
    _time_tree = models.OneToOneField(TimeTree, blank=True, null=True, on_delete=models.SET_NULL)
    _goals = models.ManyToManyField(Goal, related_name='_jobs')
    # Other fields
    description = models.TextField(default='')
    is_done = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_savable = self.is_savable()
        if is_savable is True:
            super(Job, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
            return True
        else:
            return is_savable

    def is_savable(self):
        is_is_done_valid = self.is_is_done_valid()
        if is_is_done_valid is True:
            return True
        else:
            error_message = is_is_done_valid[1]

        return False, error_message

    def is_is_done_valid(self):
        if self.id is not None:
            if self.is_done is False:
                for goal in self._goals:
                    if goal.is_achieved is True:
                        return False, 'Goal is achieved before its job is done'

            # No objection -> is_achieved valid
            return True
        else:
            return True

    def is_timewise_valid(self):
        # Not saved yet
        if self.id is not None:
            if self._time_tree is not None and self._goals.count() > 0:
                for goal in self._goals:
                    for time_branch in self._time_tree.timebranch_set.all():
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

    def get_time_tree(self):
        return self._time_tree

    def set_time_tree(self, time_tree):
        prev_time_tree = self._time_tree
        self._time_tree = time_tree
        is_timewise_valid = self.is_timewise_valid()
        if is_timewise_valid is not True:
            self._time_tree = prev_time_tree
        return is_timewise_valid

    def all_goals(self):
        return self._goals.all()

    def add_goals(self, goals_list):
        self._goals.add(goals_list)
        is_timewise_valid = self.is_timewise_valid()
        if is_timewise_valid is not True:
            self._goals.remove(goals_list)
        return is_timewise_valid

    def remove_goals(self, goals_list):
        self._goals.remove(goals_list)

    def __str__(self):
        return str(self.id)
