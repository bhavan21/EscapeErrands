from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from errands.models import Errand, Piece, Std
from datetime import datetime as dt, timedelta as td
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect as httpRPR, HttpResponse as httpR
import json


def home(request):
    # Accessible to all
    return render(request, 'home/home.html')


def login(request):
    if request.method == 'POST':
        # Only POST request == Login
        if request.POST['Identity'] == Std.user_identity:
            request.session[Std.Keys.user_logged_in] = True
            return render(request, 'home/home.html')
        else:
            return render(request, 'home/invalid_access.html')
    else:
        # Login Page
        return render(request, 'home/login.html')


def logout(request):
    request.session[Std.Keys.user_logged_in] = False
    return render(request, 'home/home.html')
