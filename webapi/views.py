from django.shortcuts import render

from core.models.goal import Goal


class GoalCRUD:
    def __init__(self):
        pass

    @staticmethod
    def list(request):
        goal_list = Goal.objects.all()
        return render(request, 'webapi/goal/gli.html', {'goal_list': goal_list})
