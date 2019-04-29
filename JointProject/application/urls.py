from . import views
from django.urls import path, include
from django.conf.urls import url
from .views import *




urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('manifiesto_entrada/',views.manifiesto_entrada,name='manifiesto_entrada'),
    path('manifiesto_salida/', views.manifiesto_salida, name='manifiesto_salida'),
    path('salas/', views.salas, name='salas'),
    path('tareas/', views.tareas, name='tareas'),
    url(r'^manifiesto_entrada/(?P<pk>\d+)/$',
        detalls_product,
        name='detalls_product'),
]
