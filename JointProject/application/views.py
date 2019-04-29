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
    sala = Room.objects.all()
    return render(request, 'GestorSala/Sala MASS 1.html')
def salaMass2(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/Sala MASS 2.html')
def salaA(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/Sala A.html')
def salaB(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/Sala B.html')
def salaC(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/Sala C.html')
def salaM1(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/M1.html')
def salaM2(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/M2.html')
def salaM3(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/M3.html')
def salaM4(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/M4.html')
def salaM5(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/M5.html')
def salaM6(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/M6.html')
def salaF1(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F1.html')
def salaF2(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F2.html')
def salaF3(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F3.html')
def salaF4(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F4.html')
def salaF5(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F5.html')
def salaF6(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F6.html')
def salaF7(request):
    sala = Room.objects.all()
    return render(request, 'GestorSala/F7.html')

