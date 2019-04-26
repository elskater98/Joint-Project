from django.shortcuts import render
from django.shortcuts import redirect
from .models import *


def homepage(request):
    #Obtencion rol del usuario
    logged_user = request.user
    role_class = UserProfile.objects.filter(user = logged_user)

    return render(request,'generic.html',context={'role_class':role_class.get()})

# GESTOR DE SALA
def manifiesto_entrada(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala':
        manifest = Manifest.objects.filter(kind_manifest__contains='E')
        return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest':manifest,'role_class':role_class.get()})
    else:
        return redirect('/')


def manifiesto_salida(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala':
        manifest = Manifest.objects.filter(kind_manifest__contains='S')
        return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest':manifest,'role_class':role_class.get()})
    else:
        return redirect('/')

def salas(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario':
        return render(request, 'GestorSala/salas.html',context={'role_class':role_class.get()})
    else:
        return redirect('/')

def tareas(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario':
        return render(request, 'GestorSala/tareas.html',context={'role_class':role_class.get()})
    else:
        return redirect('/')
