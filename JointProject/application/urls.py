from . import views
from django.urls import path


urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('manifiesto_entrada/',views.manifiesto_entrada,name='manifiesto_entrada'),
    path('manifiesto_salida/', views.manifiesto_salida, name='manifiesto_salida'),
    path('salas/', views.salas, name='salas'),
    path('tareas/', views.tareas, name='tareas'),
    path('tarea/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('tarea/create', views.CreateTask.as_view(), name='task_create'),
    path('tarea/update_all/int<int:pk>', views.UpdateTaskAll.as_view(), name='task_update_all'),
    path('tarea/update_status/<int:pk>', views.UpdateTaskStatus.as_view(), name='task_update_status'),
]
