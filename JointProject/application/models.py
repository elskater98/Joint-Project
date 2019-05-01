from django.db import models

# Create your models here.


class Manifest(models.Model):
    date = models.DateField(null=True,blank=True,help_text="Seleccione la fecha de entrada")
    reference = models.CharField(max_length = 11)
    from_d = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True,related_name='From')
    to_d = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True,related_name='To')

    MANIFEST_STATUS =(('E','Entrada'),('S','Salida'))
    kind_manifest = models.CharField(max_length=1,choices=MANIFEST_STATUS,blank=False,default='E')

    def __str__(self):
        return 'Ref: %s ( %s )' % (self.reference,self.date)


class Address(models.Model):

    address = models.CharField(max_length=64, help_text="Inserte la direccion")
    postal_code = models.CharField(max_length=5, help_text="Inserte el codigo postal")

    def __str__(self):
        return 'Postal Code: %s - Address: %s' % (self.postal_code, self.address)


class Dimension (models.Model):
    long_cm = models.IntegerField()
    width_cm = models.IntegerField()
    height_cm = models.IntegerField()

    def __str__(self):
        return '%s x %s x %s' % (self.long_cm, self.width_cm, self.height_cm)


class Level_Agreement (models.Model):
    temp_max = models.IntegerField()
    temp_min = models.IntegerField()
    hum_max = models.IntegerField()
    hum_min = models.IntegerField()

    def __str__(self):
        return 'temp: (%s - %s) hum:( %s - %s )' % (self.temp_max,self.temp_min,self.hum_max,self.hum_min)

class Client (models.Model):
    DNI = models.CharField(max_length=9)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    lives_in = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='domicili')

    def __str__(self):
        return ' %s %s ' % (self.name, self.surname)


class Product (models.Model):
    name = models.CharField(max_length=64)
    delivery_date = models.DateField(null=True,blank=True,help_text="Seleccionar la fecha de salida")
    level_agreement = models.ForeignKey(Level_Agreement,related_name='te',on_delete=models.PROTECT,default='0')
    client = models.ForeignKey(Client, related_name='es_de', on_delete=models.PROTECT, default='0')

    def __str__(self):
        return '%s ( %s - %s )' % (self.name,self.delivery_date, self.client)


class Room (models.Model):
    nombre = models.CharField(max_length=64)
    temperatura = models.IntegerField()
    ancho = models.IntegerField()
    largo = models.IntegerField()
    espacio_Total = models.IntegerField()
    espacio_Ocupado = models.IntegerField()

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