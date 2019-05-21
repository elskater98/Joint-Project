from django.views.generic import ListView
from . import views
from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('manifiesto_entrada/', views.manifiesto_entrada, name='manifiesto_entrada'),
    path('manifiesto_entrada/manifest', views.api_request, name='api_request'),
    path('manifiesto_salida/', views.manifiesto_salida, name='manifiesto_salida'),
    url(r'^salas/$',
        ListView.as_view(
            queryset=Room.objects.all(),  # bases de dades
            context_object_name='rooms',  # nom del diccionari
            template_name='GestorSala/rooms.html'),  # posem el nom del html i on ho va a buscar
        name='rooms'),

    url(r'^salas/(?P<pk>\d+)/$',
        detalls_sala,
        name='detalls_sala'),

    url(r'^manifiesto_entrada/(?P<pk>\d+)/$',
        detalls_product,
        name='detalls_product'),
    path('salas/', views.salas, name='salas'),
    #VISTA
    path('tareas/mantenimiento', views.tareas_mantenimiento, name='tareas_mantenimiento'),
    path('tareas/operarios', views.tareas_operarios, name='tareas_operarios'),

    #VISTA ESPECIFICA
    path('tarea/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),

    #CREATE
    path('tarea/create_task', views.CreateTask.as_view(), name='task_create'),

    #UPDATE
    path('tarea/update_all/int<int:pk>', views.UpdateTaskAll.as_view(), name='task_update_all'),
    path('tarea/update_status/<int:pk>', views.UpdateTaskStatus.as_view(), name='task_update_status'),
    path('tarea/update_assigned/<int:pk>', views.UpdateAssignedTask.as_view(), name='task_update_assigned'),

    #DELETE
    path('tarea/delete_task/<int:pk>', views.DeleteTask.as_view(), name='task_delete'),

    #VISTA MANIFESTOS
    path('tarea/create_task', views.CreateTask.as_view(), name='task_create'),


]
