from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from application.forms import TaskForm
from .models import *

import json
import urllib.request
from bs4 import BeautifulSoup


def api_request(request):
    # https: // stackoverflow.com / questions / 44239822 / urllib - request - urlopenurl -with-authentication / 44239906
        logged_user = request.user
        role_class = UserProfile.objects.filter(user=logged_user)

        reference = request.POST.get('search', '')

        # print(referencia)
    # if role_class.get().role == 'gestorsala':
        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        top_level_url = "https://ourfarms.herokuapp.com/apiRest/REF/?ref="+reference
        password_mgr.add_password(None, top_level_url, "GR2", "gr2134567890")

        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        # create "opener" (OpenerDirector instance)
        opener = urllib.request.build_opener(handler)

        # use the opener to fetch a URL
        products = opener.open("https://ourfarms.herokuapp.com/apiRest/REF/?ref="+reference)

        soup = BeautifulSoup(products.read(), 'html.parser')
        data = json.loads(soup.decode("utf-8"))   # items -> type list data is a list of the manifests

        if data:  # comproves si la llista NO es buida, si ho es, es que la ref no es correcta
            # print(type(data))
            for manifest in data:
                for key, value in manifest.items():  # busquem tots els productes diferents dins el manifest
                    if key == "ref":
                        ref = value
                    elif key == "withdrawal":
                        withdrawal = value
                    elif key == "fromLocation":
                        fromLocation = value
                    elif key == "toLocation":
                        toLocation = value
                    elif key == "totalpackets":
                        totalpackets = value
                    elif key == "Products":
                        # print("I'm manifest",referencia,"and I have ", len(value), "products")  # value is a list
                        for x in range(len(value)):  # iterem per cada producte que hi ha per veure els atributs
                            # print("Product: ", x, "-->", value[x])
                            for key_product, value_product in value[x].items():  # per para atribut que hi ah dels productes els guardem als models
                                # print(key_product,value_product)
                                if key_product == "name":
                                    name = value_product
                                elif key_product == "qty":
                                    qty = value_product
                                elif key_product == "tempMaxDegree":
                                    tempMaxDegree = value_product
                                elif key_product == "tempMinDegree":
                                    tempMinDegree = value_product
                                elif key_product == "humidMax":
                                    humidMax = value_product
                                elif key_product == "humidMin":
                                    humidMin = value_product
                                elif key_product == "sla":
                                    sla = value_product

                            newproduct = Product(name=name, reference=reference, qty=qty, temp_max=tempMaxDegree, temp_min=tempMinDegree,
                                                  hum_max=humidMax, hum_min=humidMin, sla=sla)

                            newproduct.save()

                newmanifest = Manifest(reference=ref, withdrawal=withdrawal, fromLocation=fromLocation, toLocation=toLocation, totalPackets=totalpackets)
                newmanifest.save()

                product = Product.objects.filter(reference=reference)
                manifest = Manifest.objects.filter(reference=reference)

            return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest': manifest, 'role_class': role_class.get()})
        else:
            manifest = []
            return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest': manifest, 'role_class': role_class.get()})


class ApiReq (LoginRequiredMixin, DetailView):
    template_name = 'GestorSala/detalls_product.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ApiReq, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'operario' or role == 'mantenimiento':
            return super(ApiReq, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def homepage(request):
    # Obtencion rol del usuario
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    return render(request, 'generic.html', context={'role_class': role_class.get()})


def manifiesto_entrada(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala'or role_class.get().role == 'admin' or role_class.get().role == 'CEO':
        manifest = Manifest.objects.filter(withdrawal=True)
        return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest': manifest, 'role_class': role_class.get()})
    else:
        return redirect('/')


def manifiesto_salida(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'CEO':
        manifest = Manifest.objects.filter(withdrawal=False)
        return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest': manifest, 'role_class': role_class.get()})
    else:
        return redirect('/')


def detalls_sala(request, pk):
    room = Room.objects.get(pk=pk)
    containers = Container.objects.filter(room=room)
    dictio = {'containers': containers,
              'room': room}
    return render(request=request, template_name="GestorSala/detalls_sala.html", context=dictio)


def detalls_product(request, pk):
    manifest = Manifest.objects.get(pk=pk)
    products = Product.objects.filter(manifest=manifest.reference)
    dictio = {'products': products,
              'manifest': manifest}
    return render(request=request, template_name="GestorSala/detalls_product.html", context=dictio)


def salas(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario' or role_class.get().role == 'admin':
        return render(request, 'GestorSala/salas.html',context={'role_class':role_class.get()})
    else:
        return redirect('/')


def tareas_mantenimiento(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'mantenimiento' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P').filter(t_status__contains='M')
        tasks_r = Task.objects.filter(status__contains='R').filter(t_status__contains='M')
        tasks_f = Task.objects.filter(status__contains='F').filter(t_status__contains='M')
        return render(request, 'GestorSala/tareas.html', context={'role_class':role_class.get(), 'tareas_p':tasks_p, 'tareas_r':tasks_r, 'tareas_f':tasks_f})
    else:
        return redirect('/')


def tareas_operarios(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P').filter(t_status__contains='O')
        tasks_r = Task.objects.filter(status__contains='R').filter(t_status__contains='O')
        tasks_f = Task.objects.filter(status__contains='F').filter(t_status__contains='O')
        return render(request, 'GestorSala/tareas.html', context={'role_class':role_class.get(), 'tareas_p':tasks_p, 'tareas_r':tasks_r, 'tareas_f':tasks_f})
    else:
        return redirect('/')


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