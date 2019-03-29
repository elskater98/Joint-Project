from django.shortcuts import render
from .models import *


def start_page(request):
    return render(request, 'start_page.html')

def availableAction(request):
    return render(request,'availableActions.html')

def generateTasks(request):
    return render(request,'generateTasks.html')

def roomManager(request):
    return render(request,'roomManager.html')

def ceo(request):
    return render(request,'ceo.html')

def workers(request):
    return render(request,'workers.html')

def maitenance(request):
    return render(request,'maintenance.html')

def manifest(request):
    return render(request,'manifest.html')

def ver_mod_propDistr(request):
    return render(request,'verify-modify_proposedDistribution.html')