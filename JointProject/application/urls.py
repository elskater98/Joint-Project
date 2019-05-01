from . import views
from django.urls import path


urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('manifiesto_entrada/',views.manifiesto_entrada,name='manifiesto_entrada'),
    path('manifiesto_salida/', views.manifiesto_salida, name='manifiesto_salida'),
    path('salas/', views.salas, name='salas'),
]

#TAREA
urlpatterns+=[
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
]
