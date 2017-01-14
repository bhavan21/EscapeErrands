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
    return render(request, 'errands/all.html', {'errands': errands})


def touch(request, pk):
    # User Logged In Check
    if not request.session.get(Std.Keys.user_logged_in, False):
        return render(request, 'home/login.html')

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
        return render(request, 'home/invalid_access.html')


# TODO: validate the inputs for more security
def process_touch(request):
    # User Logged In Check
    if not request.session.get(Std.Keys.user_logged_in, False):
        return render(request, 'home/login.html')

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
        return render(request, 'home/invalid_access.html')


def delete(request):
    # User Logged In Check
    if not request.session.get(Std.Keys.user_logged_in, False):
        return render(request, 'home/login.html')

    if request.method == 'POST':
        if 'pk' in request.POST:
            try:
                delete_errand = Errand.objects.get(pk=request.POST['pk'])
                delete_errand.delete()
                return httpRPR(reverse('errands:all'))
            except ObjectDoesNotExist:
                return render(request, 'home/invalid_access.html')
    else:
        return render(request, 'home/invalid_access.html')


def fetch_errand(request, pk):
    try:
        errand = Errand.objects.get(pk=pk)
        piece_descriptions = []
        pieces = errand.piece_set.all()
        for piece in pieces:
            piece_description = json.loads(piece.description)
            piece_description['pk'] = piece.pk
            piece_descriptions.append(piece_description)

    except ObjectDoesNotExist:
        return httpR(-1)

    errand_description = json.loads(errand.description)
    errand_description['pk'] = errand.pk

    json_string = json.dumps({'errand': errand_description, 'pieces': piece_descriptions})
    return httpR(json_string)


def fetch_piece(request, pk):
    try:
        piece = Piece.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return httpR(-1)

    desc = json.loads(piece.description)
    desc['pk'] = piece.pk
    desc['errand_pk'] = piece.errand_id
    desc['errand_tag'] = piece.errand.tag
    json_string = json.dumps(desc)
    return httpR(json_string)


def intersect(e1, e2):
    e1_epoch = e1['epoch']
    e2_epoch = e2['epoch']
    e1_end = e1['end']
    e2_end = e2['end']
    return e1_epoch < e2_epoch < e1_end or e1_epoch < e2_end < e1_end or e2_epoch < e1_epoch < e2_end or e2_epoch < e1_end < e2_end


def fetch_stubs(request):
    if 'LB' in request.GET and 'UB' in request.GET:
        try:
            lb = dt.strptime(request.GET['LB'], Std.input_dt_format)
            ub = dt.strptime(request.GET['UB'], Std.input_dt_format)
        except ValueError:
            return httpR(-1)

        event_stubs = []
        lanes = []
        task_stubs = []

        all_pieces = Piece.objects.all()
        # Creating Stubs within the given Time Range
        for piece in all_pieces:
            # Non Repeating
            if piece.is_non_repeating():
                epoch = dt.combine(piece.epoch_date, piece.epoch_time)
                stub = piece.get_stub_which_intersects(epoch, lb, ub)
                if stub is not None:
                    # Task Stub
                    if piece.is_task():
                        task_stubs.append(stub)
                    # Event Stub
                    else:
                        event_stubs.append(stub)
            # Repeating
            else:
                init_epoch = dt.combine(piece.epoch_date, piece.epoch_time)
                duration = piece.duration
                # Non - Zero Time Period
                time_period = piece.time_period
                # Starting from init_epoch
                i_epoch = init_epoch
                i_end = i_epoch + duration
                # Travelling from init_epoch to the first possible intersection
                while i_end <= lb:
                    i_end += time_period
                i_epoch = i_end - duration

                # Adding stubs
                # Task Stubs (Once a task piece always a task piece)
                if piece.is_task():
                    # Until epoch goes above the upper bound
                    while i_epoch < ub:
                        # Adding Stubs one by one
                        stub = piece.get_stub_which_intersects(i_epoch, lb, ub)
                        if stub is not None:
                            task_stubs.append(stub)
                        i_epoch += time_period
                # Event Stubs (Once a event piece always a event piece)
                else:
                    # Until epoch goes above the upper bound
                    while i_epoch < ub:
                        # Non Repeating
                        stub = piece.get_stub_which_intersects(i_epoch, lb, ub)
                        if stub is not None:
                            event_stubs.append(stub)
                        i_epoch += time_period

        # Ordering stubs , Creating lanes
        for stub in event_stubs:

            in_some_lane = False
            for lane in lanes:
                in_this_lane = True
                for car in lane:
                    if intersect(stub, car):
                        in_this_lane = False
                        break
                # If intersect with no car in this lane
                # Then add the stub in this lane
                if in_this_lane:
                    lane.append(stub)
                    in_some_lane = True
                    break

            # If not in some lane
            # Add a lane
            # Add this stub in that lane
            if not in_some_lane:
                lanes.append([stub])

        # Serializing datetime to json format
        for lane in lanes:
            for stub in lane:
                stub['epoch'] = stub['epoch'].strftime(Std.output_dt_format),
                stub['end'] = stub['end'].strftime(Std.output_dt_format),

        for task_stub in task_stubs:
            task_stub['epoch'] = task_stub['epoch'].strftime(Std.output_dt_format),
            task_stub['end'] = task_stub['end'].strftime(Std.output_dt_format),

        json_string = json.dumps({'Lanes': lanes, 'Task_Stubs': task_stubs})
        return httpR(json_string)
    else:
        return httpR(-1)
