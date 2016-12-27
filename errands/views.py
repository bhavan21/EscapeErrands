from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from models import Errand, Piece, Std
from datetime import datetime as dt, timedelta as td
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect as httpRPR, HttpResponse as httpR
import json


def all_(request):
    errands = Errand.objects.all()
    return render(request=request, template_name='errands/all.html', context={'errands': errands})


def touch(request, pk):
    # pk >= 0 from regex
    int__pk = int(pk)

    if request.method == 'GET':
        # New errand
        if int__pk == 0:
            errand = None
            old_pieces = []

            return render(request, 'errands/touch.html', {'errand': errand,
                                                          'old_pieces': old_pieces,
                                                          })
        # Old errand
        else:
            errand = get_object_or_404(Errand, pk=pk)
            old_pieces = []
            for piece in errand.piece_set.all():
                piece.epoch_date = piece.epoch_date.strftime(Std.output_d_format)
                piece.epoch_time = piece.epoch_time.strftime(Std.output_t_format)
                old_pieces.append(piece)

            return render(request, 'errands/touch.html', {'errand': errand,
                                                          'old_pieces': old_pieces,
                                                          })
    else:
        return httpR('Invalid Access')


# TODO: validate the inputs for more security
def process_touch(request):
    # pk >= 0 from regex
    if request.method == 'POST':

        int__flag = int(request.POST['Flag'])
        input_errand = json.loads(request.POST['Errand'])
        input_old_pieces = json.loads(request.POST['Old_Pieces'])
        input_new_pieces = json.loads(request.POST['New_Pieces'])

        # New Errand
        if input_errand[Std.Keys.pk] == 0:
            # new errand
            errand = Errand()
            errand.set(tag=input_errand[Std.Keys.tag],
                       comment=input_errand[Std.Keys.comment],
                       misc={})
            errand.save()

            for input_new_piece in input_new_pieces:
                new_piece = Piece()
                new_piece.set(tag=input_new_piece[Std.Keys.tag],
                              comment=input_new_piece[Std.Keys.comment],
                              misc={},
                              epoch_date=dt.strptime(input_new_piece[Std.Keys.epoch_date], Std.input_d_format).date(),
                              epoch_time=dt.strptime(input_new_piece[Std.Keys.epoch_time], Std.input_t_format).time(),
                              time_period=td(days=int(input_new_piece[Std.Keys.time_period][Std.Keys.days]),
                                             seconds=int(input_new_piece[Std.Keys.time_period][Std.Keys.seconds])
                                             ),
                              duration=td(days=int(input_new_piece[Std.Keys.duration][Std.Keys.days]),
                                          seconds=int(input_new_piece[Std.Keys.duration][Std.Keys.seconds])
                                          ),
                              )
                new_piece.save()
                errand.piece_set.add(new_piece)
        # Old Errand
        else:
            # (possible) old errand
            errand = get_object_or_404(Errand, pk=input_errand[Std.Keys.pk])
            errand.set(tag=input_errand[Std.Keys.tag],
                       comment=input_errand[Std.Keys.comment],
                       misc={})
            errand.save()

            old_pieces = errand.piece_set.all()
            updated_pks = []

            # Update Old Pieces
            for input_old_piece in input_old_pieces:
                # take a look on updated pieces
                updated_pks.append(int(input_old_piece[Std.Keys.pk]))
                # updating old pieces
                old_piece = Piece.objects.get(pk=input_old_piece[Std.Keys.pk])
                old_piece.set(tag=input_old_piece[Std.Keys.tag],
                              comment=input_old_piece[Std.Keys.comment],
                              misc={},
                              epoch_date=dt.strptime(input_old_piece[Std.Keys.epoch_date], Std.input_d_format).date(),
                              epoch_time=dt.strptime(input_old_piece[Std.Keys.epoch_time], Std.input_t_format).time(),
                              time_period=td(days=int(input_old_piece[Std.Keys.time_period][Std.Keys.days]),
                                             seconds=int(input_old_piece[Std.Keys.time_period][Std.Keys.seconds])
                                             ),
                              duration=td(days=int(input_old_piece[Std.Keys.duration][Std.Keys.days]),
                                          seconds=int(input_old_piece[Std.Keys.duration][Std.Keys.seconds])
                                          ),
                              )
                old_piece.save()

            # Delete Old Pieces
            for old_piece in old_pieces:
                # Check whether it is updated or not
                delete_this = True
                for updated_pk in updated_pks:
                    if updated_pk == old_piece.pk:
                        print (updated_pk)
                        delete_this = False
                        break
                # Not updated then delete
                if delete_this:
                    old_piece.delete()

            # Create New Pieces
            for input_new_piece in input_new_pieces:
                new_piece = Piece()
                new_piece.set(tag=input_new_piece[Std.Keys.tag],
                              comment=input_new_piece[Std.Keys.comment],
                              misc={},
                              epoch_date=dt.strptime(input_new_piece[Std.Keys.epoch_date], Std.input_d_format).date(),
                              epoch_time=dt.strptime(input_new_piece[Std.Keys.epoch_time], Std.input_t_format).time(),
                              time_period=td(days=int(input_new_piece[Std.Keys.time_period][Std.Keys.days]),
                                             seconds=int(input_new_piece[Std.Keys.time_period][Std.Keys.seconds])
                                             ),
                              duration=td(days=int(input_new_piece[Std.Keys.duration][Std.Keys.days]),
                                          seconds=int(input_new_piece[Std.Keys.duration][Std.Keys.seconds])
                                          ),
                              )
                new_piece.save()
                errand.piece_set.add(new_piece)

        if int__flag == 1:
            return httpRPR(reverse('errands:all'))
        elif int__flag == 0:
            return httpRPR(reverse('errands:touch', kwargs={'pk': errand.pk}))

    else:
        return httpR('Invalid Access')


def delete(request):
    if request.method == 'POST':
        if 'pk' in request.POST:
            try:
                delete_errand = Errand.objects.get(pk=request.POST['pk'])
                delete_errand.delete()
            except ObjectDoesNotExist:
                pass
        return httpRPR(reverse('errands:all'))
    else:
        return httpR('Invalid Access')
