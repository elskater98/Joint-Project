from django.conf.urls import url
from django.views.generic import ListView

from application.models import Room
from application.views import detalls_sala
from . import views
from django.urls import path, include
from django.conf.urls import url
from .views import *




urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('manifiesto_entrada/',views.manifiesto_entrada,name='manifiesto_entrada'),
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

    path('tareas/', views.tareas, name='tareas'),

    url(r'^manifiesto_entrada/(?P<pk>\d+)/$',
        detalls_product,
        name='detalls_product'),
]
