from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

# Create your views here.
from application.models import UserProfile
from create_user.forms import SignUpForm


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('homepage')
    template_name = 'Registration/signup.html'

def AllUsers(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)

    operarios = User.objects.all().filter(profile__role='operario')
    mantenimiento = User.objects.all().filter(profile__role='mantenimiento')
    gestorsala = User.objects.all().filter(profile__role='gestorsala')
    CEO = User.objects.all().filter(profile__role='CEO')

    return render(request, 'details/user_detail.html', context={'role_class': role_class.get(),'operarios':operarios,'mantenimiento':mantenimiento,'gestorsala':gestorsala,'CEO':CEO})

class UpdateUser(UpdateView):
    template_name = 'update/update_task.html'
    model = User
    success_url = reverse_lazy('all_users')
    fields = ['username', 'first_name', 'last_name', 'email']

class UpdateRole(UpdateView):
    template_name = 'update/update_task.html'
    success_url = reverse_lazy('all_users')
    model = UserProfile
    fields = ['role']
