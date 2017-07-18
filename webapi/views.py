from django.http import HttpResponse
from django.shortcuts import render
from modelforms import TimeBranchForm


class TimeBranchCRUD:
    @staticmethod
    def create(request):
        if request.method == 'POST':
            form = TimeBranchForm(request.POST)
            if form.is_valid() is True:
                return HttpResponse(form.cleaned_data)

        else:
            form = TimeBranchForm()

        return render(request, 'webapi/timebranch/create.html', {'form': form})

    def __init__(self):
        pass
