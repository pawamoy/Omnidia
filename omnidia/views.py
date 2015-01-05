from django.shortcuts import render


def home(request):
    return render(request, 'model/home.html', locals())
