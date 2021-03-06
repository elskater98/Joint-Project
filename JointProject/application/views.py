from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from application.forms import TaskForm
from application.models import Container, Task
from application.forms import TaskForm,CEOForm
from .models import *

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import json
import urllib.request
from bs4 import BeautifulSoup


list_manifests = []
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

    if reference not in list_manifests:
        list_manifests.append(reference)
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
                                    sla = value_product[:10]

                            newproduct = Product(name=name, reference=reference, qty=qty, temp_max=tempMaxDegree, temp_min=tempMinDegree,
                                                  hum_max=humidMax, hum_min=humidMin, sla=sla)

                            newproduct.save()
                    elif key == "creationDate":
                        creationDate = value[:10]
                    elif key == "revisionDate":
                        revisionDate = value[:10]

                newmanifest = Manifest(reference=ref, withdrawal=withdrawal, fromLocation=fromLocation, toLocation=toLocation,
                                       totalPackets=totalpackets, creationDate=creationDate, revisionDate=revisionDate)
                newmanifest.save()

                product = Product.objects.filter(reference=reference)
                manifest = Manifest.objects.filter(reference=reference)

            return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest': manifest, 'role_class': role_class.get()})
        else:
            manifest = []
            return render(request, 'GestorSala/manifiesto_entrada.html', context={'manifest': manifest, 'role_class': role_class.get()})
    else:

        return render(request, 'GestorSala/manifiesto_entrada.html',context={'role_class': role_class.get()})

class ApiReq (LoginRequiredMixin, DetailView):
    template_name = 'details/product_detail.html'

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
        raise PermissionDenied


class ManifiestoDetail(DetailView):
    template_name = 'details/manifest_detail.html'
    model = Manifest

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'CEO':
            return super(ManifiestoDetail, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



def manifiesto_salida(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'CEO':
        manifest = Manifest.objects.filter(withdrawal=False)
        return render(request, 'GestorSala/manifiesto_salida.html', context={'manifest': manifest, 'role_class': role_class.get()})
    else:
        raise PermissionDenied


def room_details(request, pk):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' \
            or role_class.get().role == 'CEO' or role_class.get().role == 'mantenimiento' \
            or role_class.get().role == 'operario':
        room = Room.objects.get(pk=pk)
        containers = Container.objects.filter(room=room)
        return render(request=request, template_name="details/room_detail.html", context={'containers': containers, 'room': room})
    else:
        raise PermissionDenied

def room_tareas(request, pk):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'CEO' or role_class.get().role == 'mantenimiento' or role_class.get().role == 'operario':
        room = Room.objects.get(pk=pk)
        tareas = Task.objects.filter(sala=room)
        return render(request=request, template_name="details/room_tasks.html", context={'tareas': tareas, 'room': room})
    else:
        raise PermissionDenied


def product_details(request, pk):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'admin' or role_class.get().role == 'operario':
        reference = pk
        products = Product.objects.filter(reference=reference)
        return render(request=request, template_name="details/product_detail.html",
                      context={'products': products, 'reference': reference})
    else:
        raise PermissionDenied


def rooms(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'mantenimiento' or \
            role_class.get().role == 'admin' or role_class.get().role == 'operario':
        rooms_c = Room.objects.filter(room_status__contains='F')  # Cold
        rooms_m = Room.objects.filter(room_status__contains='M')  # Mixed
        rooms_n = Room.objects.filter(room_status__contains='N')  # Normal
        return render(request, 'GestorSala/rooms.html', context={'role_class': role_class.get(), 'cold': rooms_c,
                                                                 'mixed': rooms_m, 'normal': rooms_n})

    else:
        raise PermissionDenied


"""
class ListRooms(ListView):
    queryset = Room.objects.all()
    context_object_name = 'rooms'
    template_name = 'GestorSala/rooms.html'

    def dispatch(self, request, *args, **kwargs):
        Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'CEO' or role == 'operario' or role == 'mantenimiento':
            return super(ListRooms, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
"""


def tareas_mantenimiento(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'mantenimiento' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P').filter(t_status__contains='M').filter(ocultar='False')
        tasks_r = Task.objects.filter(status__contains='R').filter(t_status__contains='M').filter(ocultar='False')
        tasks_f = Task.objects.filter(status__contains='F').filter(t_status__contains='M').filter(ocultar='False')

        return render(request, 'GestorSala/tareas.html', context={'role_class':role_class.get(), 'tareas_p':tasks_p, 'tareas_r':tasks_r, 'tareas_f':tasks_f})
    else:
        raise PermissionDenied


def tareas_operarios(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'gestorsala' or role_class.get().role == 'operario' or role_class.get().role == 'admin':
        tasks_p = Task.objects.filter(status__contains='P').filter(t_status__contains='O').filter(ocultar='False')
        tasks_r = Task.objects.filter(status__contains='R').filter(t_status__contains='O').filter(ocultar='False')
        tasks_f = Task.objects.filter(status__contains='F').filter(t_status__contains='O').filter(ocultar='False')
        return render(request, 'GestorSala/tareas.html', context={'role_class':role_class.get(), 'tareas_p':tasks_p, 'tareas_r':tasks_r, 'tareas_f':tasks_f})
    else:
        raise PermissionDenied


def ceo_reports(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'CEO' or role_class.get().role == 'admin':
        return render(request, 'CEO/reports.html', context={'role_class': role_class.get()})
    else:
        raise PermissionDenied


def ceo_analysis(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'CEO' or role_class.get().role == 'admin':
        doc = Documents.objects.all()
        return render(request, 'CEO/analysis.html', context={'role_class': role_class.get(),'doc':doc})
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

    template_name = 'create/create_task.html'


    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(CreateTask, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        status = form.cleaned_data['t_status']
        if status == 'O':
            return redirect(reverse('tareas_operarios'))
        else:
            return redirect(reverse('tareas_mantenimiento'))

class UpdateTaskAll(LoginRequiredMixin,UpdateView):
    template_name = 'update/update_task.html'
    model = Task
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(UpdateTaskAll, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        """Solo se pueden selecionar usuarios con  el rol gestor de sala o operario"""
        context = super(UpdateTaskAll,self).get_context_data(**kwargs)
        context['form'].fields['assigned'].queryset = UserProfile.objects.filter(role='operario')| UserProfile.objects.filter(role='mantenimiento')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        status = form.cleaned_data['t_status']
        if status == 'O':
            return redirect(reverse('tareas_operarios'))
        else:
            return redirect(reverse('tareas_mantenimiento'))




class UpdateAssignedTask(LoginRequiredMixin,UpdateView):
    template_name = 'update/update_task.html'
    model = Task
    fields = ['t_status','assigned']

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

    fields = ['t_status','status']

    def dispatch(self, request, *args, **kwargs):
        """Solo puede hacer uso de la clase aquellos usuarios con un rol disponible"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'operario' or role == 'mantenimiento':
            return super(UpdateTaskStatus, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        status = form.cleaned_data['t_status']
        if status == 'O':
            return redirect(reverse('tareas_operarios'))
        else:
            return redirect(reverse('tareas_mantenimiento'))

class UpdateTasktoFinish(LoginRequiredMixin, UpdateView):
    template_name = 'update/update_task.html'
    model = Task
    fields = ['t_status','ocultar']

    def dispatch(self, request, *args, **kwargs):
        """Solo puede hacer uso de la clase aquellos usuarios con un rol disponible"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala' or role == 'operario' or role == 'mantenimiento':
            return super(UpdateTasktoFinish, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        status = form.cleaned_data['t_status']
        if status == 'O':
            return redirect(reverse('tareas_operarios'))
        else:
            return redirect(reverse('tareas_mantenimiento'))

class DeleteTask(LoginRequiredMixin,DeleteView):
    template_name = 'delete/delete_task.html'
    model = Task


    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(DeleteTask, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



class ChangeRoom(LoginRequiredMixin,UpdateView):
    template_name = 'update/update_task.html'
    model = Container
    fields = ['room']
    success_url = '/application/salas/'
    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'gestorsala':
            return super(ChangeRoom, self).dispatch(request, *args, **kwargs)
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
    template_name = 'CEOf.html'

    def dispatch(self, request, *args, **kwargs):
        """Solo puede acceder a la creacion de una tarea los usuarios con el rol gestor de sala o admin"""
        role = self.request.user.profile.role
        if role == 'admin' or role == 'CEO':
            return super(ListForms, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def CEOflist(request):

    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    if role_class.get().role == 'admin' or role_class.get().role == 'CEO':
        form = CEOf.objects.all()
        return render(request=request, template_name="CEOf.html",
                      context={'CEOf': form})
    else:
        raise PermissionDenied

class DeletefCEO(LoginRequiredMixin,DeleteView):
    template_name = 'delete/CEOf_delete.html'
    model = CEOf
    success_url = '/application/'

    def dispatch(self, request, *args, **kwargs):
        role = self.request.user.profile.role
        if role == 'admin' or role == 'CEO':
            return super(DeletefCEO, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
