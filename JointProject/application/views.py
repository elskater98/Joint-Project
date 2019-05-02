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

def detalls_sala(request, pk):
    room = Room.objects.get(pk=pk)
    containers = Container.objects.filter(room=room)
    dictio = {'containers': containers,
              'room': room}
    return render(request=request, template_name="GestorSala/detalls_sala.html", context=dictio)

def tareas(request):
    return render(request, 'GestorSala/tareas.html',)

def detalls_product (request, pk):
    manifest = Manifest.objects.get(pk=pk)
    products = Product.objects.filter(manifest=manifest.reference)
    dictio = {'products': products,
              'manifest': manifest}
    return render(request=request, template_name="GestorSala/detalls_product.html", context=dictio)
