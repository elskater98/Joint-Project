from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView,ListView

from application.forms import TaskForm,CEOForm
from .models import *


def homepage(request):
    # Obtencion rol del usuario
    logged_user = request.user
    role_class = UserProfile.objects.filter(user = logged_user)

    return render(request,'generic.html',context={'role_class':role_class.get()})


def manifiesto_entrada(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala'or role_class.get().role == 'admin' or role_class.get().role == 'CEO':
        manifest = Manifest.objects.filter(kind_manifest__contains='E')
        return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest':manifest,'role_class':role_class.get()})
    else:
        raise PermissionDenied


def manifiesto_salida(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'CEO':
        manifest = Manifest.objects.filter(kind_manifest__contains='S')
        return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest':manifest,'role_class':role_class.get()})
    else:
        raise PermissionDenied

def room_details(request, pk):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'CEO' or role_class.get().role == 'mantenimiento' or role_class.get().role == 'operario':
        room = Room.objects.get(pk=pk)
        containers = Container.objects.filter(room=room)
        return render(request=request, template_name="details/room_detail.html", context={'containers': containers,'room': room})
    else:
        raise PermissionDenied


def product_details (request, pk):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'operario':
        manifest = Manifest.objects.get(pk=pk)
        products = Product.objects.filter(manifest=manifest.reference)
        return render(request=request, template_name="details/product_detail.html", context={'products': products,'manifest': manifest})
    else:
        raise PermissionDenied

class ListRooms(ListView):
    queryset = Room.objects.all()
    context_object_name = 'rooms'
    template_name = 'GestorSala/rooms.html'

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'CEO' or role == 'operario' or role =='mantenimiento':
            return super(ListRooms, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def tareas_mantenimiento(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'mantenimiento' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P').filter(t_status__contains='M')
        tasks_r = Task.objects.filter(status__contains='R').filter(t_status__contains='M')
        tasks_f = Task.objects.filter(status__contains='F').filter(t_status__contains='M')
        return render(request, 'GestorSala/tareas.html', context={'role_class':role_class.get(), 'tareas_p':tasks_p, 'tareas_r':tasks_r, 'tareas_f':tasks_f})
    else:
        raise PermissionDenied


def tareas_operarios(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P').filter(t_status__contains='O')
        tasks_r = Task.objects.filter(status__contains='R').filter(t_status__contains='O')
        tasks_f = Task.objects.filter(status__contains='F').filter(t_status__contains='O')
        return render(request, 'GestorSala/tareas.html', context={'role_class':role_class.get(), 'tareas_p':tasks_p, 'tareas_r':tasks_r, 'tareas_f':tasks_f})
    else:
        raise PermissionDenied


class TaskDetailView(LoginRequiredMixin,DetailView):
    template_name = 'details/task_detail.html'
    model = Task

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role== 'operario' or role == 'mantenimiento':
            return super(TaskDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class CreateTask(LoginRequiredMixin,CreateView):
    form_class = TaskForm
    model = Task
    success_url = '/application/'
    template_name = 'create/create_task.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(CreateTask, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class UpdateTaskAll(LoginRequiredMixin,UpdateView):
    template_name = 'update/update_task.html'
    model = Task
    fields = '__all__'
    success_url = '/application/'

    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(UpdateTaskAll, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        """Solo se pueden selecionar usuarios con  el rol gestor de sala o operario"""
        context = super(UpdateTaskAll,self).get_context_data(**kwargs)
        context['form'].fields['assigned'].queryset = UserProfile.objects.filter(role='gestorsala')| UserProfile.objects.filter(role='admin') |UserProfile.objects.filter(role='operario')| UserProfile.objects.filter(role='mantenimiento')
        return context


class UpdateAssignedTask(LoginRequiredMixin,UpdateView):
    template_name = 'update/update_task.html'
    model = Task
    fields = ['assigned']
    success_url = '/application/'

    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role =='operario' or role == 'mantenimiento': ##Es necesario el rol de operario y mantenimiento
            return super(UpdateAssignedTask, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        """Solo se pueden selecionar usuarios con  el rol asignado"""
        context = super(UpdateAssignedTask,self).get_context_data(**kwargs)
        context['form'].fields['assigned'].queryset = UserProfile.objects.filter(role='operario')| UserProfile.objects.filter(role='mantenimiento')
        return context


class UpdateTaskStatus(LoginRequiredMixin, UpdateView):
    template_name = 'update/update_task.html'
    model = Task
    success_url = '/application/' # segons el tipus de taska Operario o manteniment redireccionar al seu propi

    fields = ['status']

    def dispatch(self, request, *args, **kwargs):
        """Solo puede hacer uso de la clase aquellos usuarios con un rol disponible"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'operario' or role == 'mantenimiento':
            return super(UpdateTaskStatus, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class DeleteTask(LoginRequiredMixin,DeleteView):
    template_name = 'delete/delete_task.html'
    model = Task
    success_url = '/application/'

    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(DeleteTask, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CreatefCEO(LoginRequiredMixin,CreateView):
    form_class = CEOForm
    model = CEOf
    success_url = '/application/'
    template_name = 'create/create_CEOf.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatefCEO, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'mantenimiento':
            return super(CreatefCEO, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CEOfDetailView(LoginRequiredMixin,DetailView):
    template_name = 'details/CEOf_detail.html'
    model = CEOf

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'CEO':
            return super(CEOfDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class ListForms(ListView):
    queryset = CEOf.objects.all()
    context_object_name = 'Ceof'
    template_name = 'CEOf.html'

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'CEO':
            return super(ListForms, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

