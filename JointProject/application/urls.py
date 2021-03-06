from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns=[
    path('',homepage,name='homepage'),
]

#MANIFIESTOS
urlpatterns+=[
    path('manifiesto/entrada/',manifiesto_entrada,name='manifiesto_entrada'),
    path('manifiesto/salida/', manifiesto_salida, name='manifiesto_salida'),
    path('manifiesto/',api_request,name='api_request'),


]

#PRODUCTO
urlpatterns+=[
    #DETAIL PRODUCT
    path('product/<int:pk>',product_details,name='product_detail'),

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
    path('tarea/update_finish/<int:pk>', UpdateTasktoFinish.as_view(), name='task_update_finish'),

    #DELETE
    path('tarea/delete_task/<int:pk>', DeleteTask.as_view(), name='task_delete'),

]

#SALAS
urlpatterns+=[
    path('salas/', rooms, name='rooms'),
    path('salas/<int:pk>', room_details, name='room_detail'),
    path('container/update/<int:pk>', ChangeRoom.as_view(), name='change_room'),
    path('salas/<int:pk>/tareas', room_tareas, name='room_tareas'),
    path('salas/<int:pk>/products',product_details,name='product_detail'),

]


#Manteniment-CEO
urlpatterns+=[
    path('formulari/',CreatefCEO.as_view(), name='formCEO_create'),
    path('formulari/<int:pk>', CEOfDetailView.as_view(), name='formCEO_detail'),
    path('form/', CEOflist, name='formCEO_list'),
    path('tarea/delete_CEOf/<int:pk>', DeletefCEO.as_view(), name='CEOf_delete'),
    path('informes/', ceo_reports, name='reports'),
    path('analisis/', ceo_analysis, name='economic_flow'),
]

