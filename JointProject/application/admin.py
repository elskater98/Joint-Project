from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Manifest)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Dimension)
admin.site.register(Level_Agreement)
admin.site.register(Container)
admin.site.register(Client)
admin.site.register(Room)
admin.site.register(Location)
admin.site.register(UserProfile)
admin.site.register(Task)




