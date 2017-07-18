from django import forms
from core.models.timebranch import TimeBranch
from core.models.timetree import TimeTree


class TimeBranchForm(forms.ModelForm):
    class Meta:
        model = TimeBranch
        fields = ['parent_tree', 'epoch', 'end', 'time_period', 'duration']

    # parent_tree = forms.ModelChoiceField(required=False, queryset=TimeTree.objects.all())
    # epoch = forms.DateTimeField(required=False)
    # end = forms.DateTimeField(required=False)
