from django.shortcuts import render


# Create your views here.
def cli(request):
    return render(request, 'cli/cli.html')
