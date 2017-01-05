from django.http import HttpResponse as httpr
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def scrolling_stubs(request):
    return render(request=request, template_name='time_table/scrolling_stubs.html')


def verbose(request):
    return httpr('Hi')
