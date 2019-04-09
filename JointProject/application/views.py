from django.shortcuts import render
from .models import *

def homepage(request):
    return render(request,'generic.html',)

def manifiesto_entrada(request):
    return render(request,'GestorSala/manifiesto_entrada.html',)

