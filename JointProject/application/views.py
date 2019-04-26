from django.shortcuts import render
from .models import *

def homepage(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user = logged_user)
    return render(request,'generic.html',context={'role':role_class.get()})

def manifiesto_entrada(request):
    manifest = Manifest.objects.filter(kind_manifest__contains='E')
    return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest':manifest})

def manifiesto_salida(request):
    manifest = Manifest.objects.filter(kind_manifest__contains='S')
    return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest':manifest})


def salas(request):
    return render(request, 'GestorSala/salas.html',)

def tareas(request):
    return render(request, 'GestorSala/tareas.html',)
