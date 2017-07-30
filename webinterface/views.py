from django.shortcuts import render


def goal_glance(request):
    return render(request, 'webinterface/goal/glance.html')
