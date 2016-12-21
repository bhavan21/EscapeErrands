from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponse
from datetime import datetime, timedelta


def home(request):



    context = {
    }
    return render(request=request, template_name='time_table/home.html', context=context)
