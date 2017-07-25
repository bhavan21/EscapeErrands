from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
import re
import json
from core.models.goal import Goal


def to_json_style(goal):
    deadline = None
    if goal.deadline is not None:
        deadline = goal.deadline.strftime('%c')
    parent_ids = []
    for parent in goal.get_parents():
        parent_ids.append(parent.id)
    child_ids = []
    for child in goal.get_children():
        child_ids.append(child.id)

    json_goal = {
        'description': goal.description,
        'deadline': deadline,
        'is_achieved': goal.is_achieved,
        'id': goal.id,
        'parent_ids': parent_ids,
        'child_ids': child_ids
    }
    return json_goal


def read_regex(request):
    if request.method == 'GET' and 'search' in request.GET:
        pattern = request.GET['search']
        try:
            re.compile(pattern)
        except re.error:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Not proper regex'}))
        matched_goals = Goal.objects.filter(description__iregex=pattern)
        json_goals = []
        for goal in matched_goals:
            json_goals.append(to_json_style(goal))

        return HttpResponse(json.dumps({'status': 0, 'body': json_goals}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'No search string in request'}))


def read_family(request, pk):
    try:
        goal = Goal.objects.get(pk=pk)
        family_of_ids = goal.get_family_set()
        json_family = []
        for member_id in family_of_ids:
            member = Goal.objects.get(pk=member_id)
            json_family.append(to_json_style(member))

        return HttpResponse(json.dumps({'status': 0, 'body': json_family}))

    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': -1, 'message': 'No goal with such id'}))
