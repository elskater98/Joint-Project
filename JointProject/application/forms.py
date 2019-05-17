from django.forms import ModelForm
from application.models import Task,CEOf


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude=('assigned',)

class CEOForm(ModelForm):
    class Meta:
        model = CEOf
        exclude=()