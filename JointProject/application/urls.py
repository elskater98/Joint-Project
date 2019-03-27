from . import views
from django.urls import path

urlpatterns=[
    path('', views.selectableRoles, name='selectableRoles'),
    # view paths
    """path('abstract/', name='abstract'),
    path('nature/', name='nature'),
    path('minimal/',views.minimal, name='minimal'),
    """

]