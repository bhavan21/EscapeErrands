from core.models.timebranch import TimeBranch
from models.timetree import TimeTree


class TimeBranchDAI:
    @staticmethod
    def create(epoch, end, time_period, duration):
        new_time_branch = TimeBranch(epoch=epoch, end=end, time_period=time_period, duration=duration)
        return new_time_branch.save()

    @staticmethod
    def set_parent_tree(time_branch_id, time_tree_id):
        try:
            time_branch = TimeBranch.objects.get(pk=time_branch_id)
            time_tree = TimeTree.objects.get(pk=time_tree_id)
            time_tree.branches.add(time_branch)
            return True
        except Exception:
            return False, 'an exception was caught'

    @staticmethod
    def set_time_fields(time_branch_id, epoch, end, time_period, duration):
        try:
            time_branch = TimeBranch.objects.get(pk=time_branch_id)
            time_branch.epoch = epoch
            time_branch.end = end
            time_branch.time_period = time_period
            time_branch.duration = duration
            return time_branch.save()
        except Exception:
            return False, 'an exception was caught'

    @staticmethod
    def delete(time_branch_id):
        try:
            time_branch = TimeBranch.objects.get(pk=time_branch_id)
            time_branch.delete()
            return True
        except Exception:
            return False, 'an exception was caught'

    @staticmethod
    def read(time_branch_id):
        try:
            return TimeBranch.objects.get(pk=time_branch_id)
        except Exception:
            return False, 'an exception was caught'

    def __init__(self):
        pass
