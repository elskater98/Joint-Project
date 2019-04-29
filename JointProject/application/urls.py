from . import views
from django.urls import path


urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('manifiesto_entrada/',views.manifiesto_entrada,name='manifiesto_entrada'),
    path('manifiesto_salida/', views.manifiesto_salida, name='manifiesto_salida'),
    path('salas/', views.salas, name='salas'),
    path('tareas/', views.tareas, name='tareas'),
    path('sala/Sala_mass_1/', views.salaMass1, name="salaMass1"),
    path('sala/Sala_mass_2/', views.salaMass2, name="salaMass2"),
    path('sala/Sala_A/', views.salaA, name="salaA"),
    path('sala/Sala_B/', views.salaB, name="salaB"),
    path('sala/Sala_C/', views.salaC, name="salaC"),
    path('sala/Sala_M1/', views.salaM1, name="salaM1"),
    path('sala/Sala_M2/', views.salaM2, name="salaM2"),
    path('sala/Sala_M3/', views.salaM3, name="salaM3"),
    path('sala/Sala_M4/', views.salaM4, name="salaM4"),
    path('sala/Sala_M5/', views.salaM5, name="salaM5"),
    path('sala/Sala_M6/', views.salaM6, name="salaM6"),
    path('sala/Sala_F1/', views.salaF1, name="salaF1"),
    path('sala/Sala_F2/', views.salaF2, name="salaF2"),
    path('sala/Sala_F3/', views.salaF3, name="salaF3"),
    path('sala/Sala_F4/', views.salaF4, name="salaF4"),
    path('sala/Sala_F5/', views.salaF5, name="salaF5"),
    path('sala/Sala_F6/', views.salaF6, name="salaF6"),
    path('sala/Sala_F7/', views.salaF7, name="salaF7"),

]
