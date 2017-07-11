# from core.models import *
#
# tree = TimeTree.objects.get(pk=1)
#
# branch = TimeBranch()
# branch.parent_tree = tree
#
# branch.duration = td(0, 3600)
# # branch.epoch = dt.now()
# branch.time_period = td(1)
# branch.end = dt.now()
#
# lp = branch.end - td(2, 600)
# up = lp + td(2)
#
# print(branch.epoch)
# print(branch.end)
# print(lp)
# print(up)
# print(branch.is_savable())
# snapshot = branch.get_snapshot(lp, up)
# print len(snapshot)
# print snapshot[0]
# print snapshot[1]
# print snapshot[2]
# # print(snapshot[0].end)

from core.models import *

x = TimeTree()
a = TimeBranch.objects.get(pk=2)
b = TimeBranch.objects.get(pk=3)
