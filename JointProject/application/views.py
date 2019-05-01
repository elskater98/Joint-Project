from django.shortcuts import render
from .models import *

def homepage(request):
    return render(request,'generic.html',)

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

def salaMass1(request):
    sala = Room.objects.filter(nombre__contains='Sala MASS 1')
    return render(request, 'GestorSala/Sala MASS 1.html', context={'sala':sala})
def salaMass2(request):
    sala = Room.objects.filter(nombre__contains='Sala MASS 2')
    return render(request, 'GestorSala/Sala MASS 2.html', context={'sala':sala})
def salaA(request):
    sala = Room.objects.filter(nombre__contains='Sala A')
    return render(request, 'GestorSala/Sala A.html', context={'sala':sala})
def salaB(request):
    sala = Room.objects.filter(nombre__contains='Sala B')
    return render(request, 'GestorSala/Sala B.html', context={'sala':sala})
def salaC(request):
    sala = Room.objects.filter(nombre__contains='Sala C')
    return render(request, 'GestorSala/Sala C.html', context={'sala':sala})
def salaM1(request):
    sala = Room.objects.filter(nombre__contains='Sala M1')
    return render(request, 'GestorSala/M1.html', context={'sala':sala})
def salaM2(request):
    sala = Room.objects.filter(nombre__contains='Sala M2')
    return render(request, 'GestorSala/M2.html',context={'sala':sala})
def salaM3(request):
    sala = Room.objects.filter(nombre__contains='Sala M3')
    return render(request, 'GestorSala/M3.html',context={'sala':sala})
def salaM4(request):
    sala = Room.objects.filter(nombre__contains='Sala M4')
    return render(request, 'GestorSala/M4.html',context={'sala':sala})
def salaM5(request):
    sala = Room.objects.filter(nombre__contains='Sala M5')
    return render(request, 'GestorSala/M5.html',context={'sala':sala})
def salaM6(request):
    sala = Room.objects.filter(nombre__contains='Sala M6')
    return render(request, 'GestorSala/M6.html',context={'sala':sala})
def salaF1(request):
    sala = Room.objects.filter(nombre__contains='Sala F1')
    return render(request, 'GestorSala/F1.html',context={'sala':sala})
def salaF2(request):
    sala = Room.objects.filter(nombre__contains='Sala F2')
    return render(request, 'GestorSala/F2.html',context={'sala':sala})
def salaF3(request):
    sala = Room.objects.filter(nombre__contains='Sala F3')
    return render(request, 'GestorSala/F3.html',context={'sala':sala})
def salaF4(request):
    sala = Room.objects.filter(nombre__contains='Sala F4')
    return render(request, 'GestorSala/F4.html',context={'sala':sala})
def salaF5(request):
    sala = Room.objects.filter(nombre__contains='Sala F5')
    return render(request, 'GestorSala/F5.html',context={'sala':sala})
def salaF6(request):
    sala = Room.objects.filter(nombre__contains='Sala F6')
    return render(request, 'GestorSala/F6.html',context={'sala':sala})
def salaF7(request):
    sala = Room.objects.filter(nombre__contains='Sala F7')
    return render(request, 'GestorSala/F7.html',context={'sala':sala})

