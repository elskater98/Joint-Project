from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView

from application.forms import TaskForm
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

    if role_class.get().role == 'gestorsala'or role_class.get().role == 'admin':
        manifest = Manifest.objects.filter(kind_manifest__contains='E')
        return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest':manifest,'role_class':role_class.get()})
    else:
        return redirect('/')


def manifiesto_salida(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin':
        manifest = Manifest.objects.filter(kind_manifest__contains='S')
        return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest':manifest,'role_class':role_class.get()})
    else:
        return redirect('/')

def salas(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario' or role_class.get().role == 'admin':
        return render(request, 'GestorSala/salas.html',context={'role_class':role_class.get()})
    else:
        return redirect('/')

def tareas(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P')
        tasks_r = Task.objects.filter(status__contains='R')
        tasks_f = Task.objects.filter(status__contains='F')
        return render(request, 'GestorSala/tareas.html',context={'role_class':role_class.get(),'tareas_p':tasks_p,'tareas_r':tasks_r,'tareas_f':tasks_f})
    else:
        return redirect('/')

class TaskDetailView(DetailView):
    template_name = 'details/task_detail.html'
    model = Task

class CreateTask(CreateView):
    form_class = TaskForm
    model = Task
    success_url = '/application/tareas'
    template_name = 'create/create_task.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


