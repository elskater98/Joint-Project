from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Manifest(models.Model):
    reference = models.CharField(max_length = 11, primary_key=True)
    fromLocation = models.CharField(max_length=64)
    toLocation = models.CharField(max_length=64)
    withdrawal = models.BooleanField()
    totalPackets = models.IntegerField()
    creationDate = models.DateField(null=True, blank=True, help_text="Seleccione la fecha de creación")
    revisionDate = models.DateField(null=True, blank=True, help_text="Seleccione la fecha de revisión")

    def __str__(self):
        return 'Ref: %s ( %s )' % (self.reference,self.creationDate)


class Dimension (models.Model):
    long_cm = models.IntegerField()
    width_cm = models.IntegerField()
    height_cm = models.IntegerField()

    def __str__(self):
        return '%s x %s x %s' % (self.long_cm, self.width_cm, self.height_cm)


class Client (models.Model):
    DNI = models.CharField(max_length=9)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)

    def __str__(self):
        return ' %s %s ' % (self.name, self.surname)


class Product (models.Model):
    reference = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    qty = models.IntegerField()
    delivery_date = models.DateField(null=True, blank=True, help_text="Seleccionar la fecha de salida")
    #client = models.ForeignKey(Client, related_name='es_de', on_delete=models.PROTECT, default='0')
    #manifest = models.ForeignKey(Manifest, related_name='es_troba', on_delete=models.PROTECT, default='0')
    temp_max = models.IntegerField()
    temp_min = models.IntegerField()
    hum_max = models.IntegerField()
    hum_min = models.IntegerField()
    sla = models.CharField(max_length=64)

    def __str__(self):
        return '%s ( %s - %s )' % (self.name, self.qty, self.reference)


class Room (models.Model):
    nombre = models.CharField(max_length=64)
    temperatura = models.IntegerField()
    ancho = models.IntegerField()
    largo = models.IntegerField()
    espacio_Total = models.IntegerField()
    espacio_Ocupado = models.IntegerField()
    desponible = models.BooleanField(default=True)

    def __str__(self):
        return '%s %iCº %ix%i %i/%i ' % (self.nombre,self.temperatura,self.ancho,self.largo,self.espacio_Ocupado,self.espacio_Total)


class Container (models.Model):
    product = models.ForeignKey(Product,related_name='conte', on_delete=models.PROTECT)
    dimension_c = models.ForeignKey(Dimension,related_name='te',on_delete=models.PROTECT)
    room = models.ForeignKey(Room, related_name='descarrega_a', on_delete=models.PROTECT)
    manifest = models.ForeignKey(Manifest, related_name='disposa_de', on_delete=models.PROTECT)

    def __str__(self):
        return '%s ( %s )' % (self.product,self.dimension_c)


class Location (models.Model):
    aisle = models.IntegerField()
    shelf = models.IntegerField()
    space = models.IntegerField()
    room = models.ForeignKey(Room,related_name='esta',on_delete=models.PROTECT)
    dimension = models.ForeignKey(Dimension, related_name='capacitat', on_delete=models.PROTECT)

    def __str__(self):
        return 'Pas:%sPres:%sH:%s-%s ' % (self.aisle,self.shelf,self.space,self.room)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile",on_delete=models.SET_DEFAULT,default=0)
    ROLE_STATUS =(('admin','admin'),('gestorsala','gestor de sala'),('operario','operario'),('mantenimiento','operario de mantenimiento'),('CEO','CEO'))
    role = models.CharField(max_length=32, choices=ROLE_STATUS, blank=False, default='operario') #Null true and blank true ?¿


    def __str__(self):
        return 'User: %s Role: %s' % (self.user,self.role)
 #Permet inclour els atributs a la clase User {{user.profile.role}}
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Task(models.Model):
    T_STATUS = (('M', 'Manteniment'), ('O', 'Operarios'))
    t_status = models.CharField(max_length=1, choices=T_STATUS, blank=False, default='O')

    TASK_STATUS = (('P', 'Pendiente'), ('R', 'Realizando'), ('F', 'Finalizada'))
    status = models.CharField(max_length=1, choices=TASK_STATUS, blank=False, default='P')

    TYPE_STATUS = (('B', 'Blanco'), ('V', 'Verde'), ('A', 'Azul'))
    tipus = models.CharField(max_length=1, choices=TYPE_STATUS, blank=False, default='V')

    assigned = models.ForeignKey(UserProfile, related_name='assignado', on_delete=models.CASCADE,null=True,blank=True) #Atribut opcional lliure eleccio per cada participant
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=256)

    ocultar = models.BooleanField(default=False)

    def __str__(self):
        return '%s ~ %s'%(self.title,self.status)

    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.id)])
