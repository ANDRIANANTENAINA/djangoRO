from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def index(request):
    return render(request, "index.html", context={"prenom": "Faly", "date": datetime.today()})


def viewTeste(request):
    return HttpResponse('<h1> Hello Word </h1>')