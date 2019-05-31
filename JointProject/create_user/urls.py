from django.urls import path

from . import views

urlpatterns=[
    path('signup',views.SignUp.as_view(),name='singup'),
    path('all_users',views.AllUsers,name='all_users'),
]