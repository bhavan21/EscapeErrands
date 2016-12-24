from django.http import HttpResponse as httpr
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from models import Errand, Piece
from django.core.exceptions import ObjectDoesNotExist


def all_(request):
    context = None
    return render(request=request, template_name='errands/all.html', context=context)


def touch(request, pk):
    if pk == '0':
        errand = {}
        old_pieces = []
    else:
        errand = {}
        old_pieces = []

    return render(request, 'errands/touch.html', {'errand': errand,
                                                  'old_pieces': old_pieces,
                                                  })
