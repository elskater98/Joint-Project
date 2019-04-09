from django.shortcuts import render
from .models import *

def homepage(request):
    return render(request,'generic.html',)

def manifiesto_entrada(request):
    manifest = Manifest.objects.filter(kind_manifest__contains='E')
    c_manifest = Manifest.objects.filter(kind_manifest__contains='E').count()
    return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest':manifest, 'range':range(c_manifest)})

def manifiesto_salida(request):
    manifest = Manifest.objects.filter(kind_manifest__contains='S')
    c_manifest = Manifest.objects.filter(kind_manifest__contains='S').count()
    return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest':manifest, 'c_manifest':c_manifest})

