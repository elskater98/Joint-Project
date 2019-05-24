from django.forms import ModelForm, forms
from application.models import Task,CEOf


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude=('assigned', 'ocultar',)

class TaskCEOForm(ModelForm):
    class Meta:
        model = Task
        exclude=('t_status','ocultar')


class CEOForm(ModelForm):
    class Meta:
        model = CEOf
        exclude=()

