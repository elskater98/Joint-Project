from django.views.generic import ListView
from django.urls import path
from .views import *

urlpatterns=[
    path('',homepage,name='homepage'),
]

#MANIFIESTOS
urlpatterns+=[
    path('manifiesto_entrada/',manifiesto_entrada,name='manifiesto_entrada'),
    path('manifiesto_salida/', manifiesto_salida, name='manifiesto_salida'),
]

#PRODUCTO
urlpatterns+=[
    path('product/<int:pk>',product_details,name='product_detail'),
]

#TAREAS
urlpatterns+=[
    #VISTA
    path('tareas/mantenimiento', tareas_mantenimiento, name='tareas_mantenimiento'),
    path('tareas/operarios', tareas_operarios, name='tareas_operarios'),

    #VISTA ESPECIFICA
    path('tarea/<int:pk>', TaskDetailView.as_view(), name='task_detail'),

    #CREATE
    path('tarea/create_task', CreateTask.as_view(), name='task_create'),

    #UPDATE
    path('tarea/update_all/<int:pk>', UpdateTaskAll.as_view(), name='task_update_all'),
    path('tarea/update_status/<int:pk>', UpdateTaskStatus.as_view(), name='task_update_status'),
    path('tarea/update_assigned/<int:pk>', UpdateAssignedTask.as_view(), name='task_update_assigned'),

    #DELETE
    path('tarea/delete_task/<int:pk>', DeleteTask.as_view(), name='task_delete'),

]

#SALAS
urlpatterns+=[
    path('salas/', ListRooms.as_view(), name='rooms'),
    path('salas/<int:pk>', room_details, name='room_detail'),
]

#Manteniment-CEO
urlpatterns+=[
    path('formulari/',CreatefCEO.as_view(), name='formCEO'),
    path('formulari/<int:pk>', CEOfDetailView.as_view(), name='CEOf_detail'),
    path('form/',ListForms.as_view(),name='formCEof')
]