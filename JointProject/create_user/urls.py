from django.urls import path

from . import views

urlpatterns=[
    path('signup',views.SignUp.as_view(),name='singup'),
    path('all_users',views.AllUsers,name='all_users'),
    path('update/<int:pk>',views.UpdateUser.as_view(),name='update_user'),
    path('update/role/<int:pk>',views.UpdateRole.as_view(),name='update_user_role'),
]