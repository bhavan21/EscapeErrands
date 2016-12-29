from django.http import HttpResponse as httpr
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


class Forms:
    class Names:
        date = 'date'
        invalid_date = 'Invalid date'

        def __init__(self):
            pass

    def __init__(self):
        pass


def home(request):
    return render(request=request, template_name='time_table/home.html')
