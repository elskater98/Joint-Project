from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from application.models import UserProfile


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'Registration/signup.html'

def AllUsers(request):
    logged_user = request.user
    role_class = UserProfile.objects.filter(user=logged_user)
    operarios = User.objects.all().filter(profile__role='operario')
    mantenimiento = User.objects.all().filter(profile__role='mantenimiento')
    gestorsala = User.objects.all().filter(profile__role='gestorsala')
    CEO = User.objects.all().filter(profile__role='CEO')

    return render(request, 'details/user_detail.html', context={'role_class': role_class.get(),'operarios':operarios,'mantenimiento':mantenimiento,'gestorsala':gestorsala,'CEO':CEO})
