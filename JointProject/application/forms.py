from django.forms import ModelForm
from application.models import Task,Container


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude=('assigned','ocultar',)