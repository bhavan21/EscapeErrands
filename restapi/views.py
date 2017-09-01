from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime as dt
from core.models.goal import Goal
import re
import json


def jsonize_goal(goal):
    deadline = None
    if goal.deadline is not None:
        deadline = {
            'year': goal.deadline.year,
            'month': goal.deadline.month,
            'day': goal.deadline.day,
            'hour': goal.deadline.hour,
            'minute': goal.deadline.minute,
            'second': goal.deadline.second,
            'microsecond': goal.deadline.microsecond,
        }
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
        'child_ids': child_ids,
        'color': goal.color,
    }
    return json_goal


def jsonize_goal_iterable(goal_ids):
    jsoned = []
    for goal_id in goal_ids:
        goal = Goal.objects.get(pk=goal_id)
        jsoned.append(jsonize_goal(goal))
    return jsoned


def read_regex(request):
    if request.method == 'GET' and 'search' in request.GET:
        pattern = request.GET['search']
        try:
            re.compile(pattern)
        except re.error:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Not proper regex'}))
        matched_goals = Goal.objects.filter(description__iregex=pattern).order_by('is_achieved', 'deadline')
        json_goals = []
        for goal in matched_goals:
            json_goals.append(jsonize_goal(goal))

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
            json_family.append(jsonize_goal(member))

        return HttpResponse(json.dumps({'status': 0, 'body': json_family}))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': -1, 'message': 'No goal with such id'}))


def create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST['data'])
            description = data['description']
            deadline = data['deadline']
            if deadline is not None:
                deadline = dt(year=deadline['year'],
                              month=deadline['month'],
                              day=deadline['day'],
                              hour=deadline['hour'],
                              minute=deadline['minute'],
                              second=deadline['second'],
                              microsecond=deadline['microsecond'])
            new_goal = Goal(description=description, deadline=deadline)
            new_goal.save()
            return HttpResponse(json.dumps({'status': 0, 'body': jsonize_goal(new_goal)}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST['data'])
            pk = data['id']
            description = data['description']
            deadline = data['deadline']
            if deadline is not None:
                deadline = dt(year=deadline['year'],
                              month=deadline['month'],
                              day=deadline['day'],
                              hour=deadline['hour'],
                              minute=deadline['minute'],
                              second=deadline['second'],
                              microsecond=deadline['microsecond'])
            existing_goal = Goal.objects.get(pk=pk)
            existing_goal.description = description
            existing_goal.deadline = deadline
            is_saved = existing_goal.save()
            if is_saved is True:
                return HttpResponse(json.dumps({'status': 0, 'body': jsonize_goal(existing_goal)}))
            else:
                return HttpResponse(json.dumps({'status': -1, 'message': is_saved[1]}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid id'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def delete_if_single(request):
    if request.method == 'POST':
        try:
            pk = request.POST['id']
            existing_goal = Goal.objects.get(pk=pk)
            if len(existing_goal.get_parents()) == 0 and len(existing_goal.get_children()) == 0:
                jsoned_goal = jsonize_goal(existing_goal)
                existing_goal.delete()
                return HttpResponse(json.dumps({'status': 0, 'body': jsoned_goal}))
            else:
                return HttpResponse(json.dumps({'status': -1, 'message': 'Goal is not single'}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid id'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def add_relation(request):
    if request.method == 'POST':
        try:
            parent_id = int(request.POST['parent_id'])
            child_id = int(request.POST['child_id'])

            parent = Goal.objects.get(pk=parent_id)
            child = Goal.objects.get(pk=child_id)
            was_relation_added = parent.add_child(child)

            if was_relation_added is True:
                new_family = parent.get_family_set()
                jsoned_new_family = jsonize_goal_iterable(new_family)
                return HttpResponse(json.dumps({'status': 0, 'body': jsoned_new_family}))
            else:
                return HttpResponse(json.dumps({'status': -1, 'message': was_relation_added[1]}))

        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid id'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def remove_relation(request):
    if request.method == 'POST':
        try:
            parent_id = int(request.POST['parent_id'])
            child_id = int(request.POST['child_id'])

            parent = Goal.objects.get(pk=parent_id)
            child = Goal.objects.get(pk=child_id)
            parent.remove_child(child)

            parent_family = parent.get_family_set()
            jsoned_parent_family = jsonize_goal_iterable(parent_family)
            body = [jsoned_parent_family]
            if child_id not in parent_family:
                child_family = child.get_family_set()
                jsoned_child_family = jsonize_goal_iterable(child_family)
                body.append(jsoned_child_family)

            return HttpResponse(json.dumps({'status': 0, 'body': body}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid id'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def toggle_is_achieved(request, pk):
    try:
        goal = Goal.objects.get(pk=pk)
        goal.is_achieved = not goal.is_achieved
        is_saved = goal.save()
        if is_saved is True:
            return HttpResponse(json.dumps({'status': 0, 'body': goal.is_achieved}))
        else:
            return HttpResponse(json.dumps({'status': -1, 'message': is_saved[1]}))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'status': -1, 'message': 'No goal with such id'}))
