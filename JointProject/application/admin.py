from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Manifest)
admin.site.register(Address)
admin.site.register(Producte)
admin.site.register(Dimensio)
admin.site.register(Level_Agreement)
admin.site.register(Container)




