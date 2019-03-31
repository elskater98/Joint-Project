from django.db import models

# Create your models here.


class Manifest(models.Model):
    date = models.DateField(null=True,blank=True,help_text="Seleccione la fecha de entrada")
    reference = models.CharField(max_length = 11)
    from_d = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True,related_name='From')
    to_d = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True,related_name='To')

    def __str__(self):
        return 'Ref: %s ( %s )' % (self.reference,self.date)


class Address(models.Model):

    address = models.CharField(max_length=64, help_text="Inserte la direccion")
    postal_code = models.CharField(max_length=5, help_text="Inserte el codigo postal")

    def __str__(self):
        return 'Postal Code: %s - Address: %s' % (self.postal_code, self.address)


class Dimensio (models.Model):
    al_cm = models.IntegerField()
    llargada_cm = models.IntegerField()
    amplada_cm = models.IntegerField()

    def __str__(self):
        return '%s x %s x %s' % (self.al_cm,self.llargada_cm,self.amplada_cm)


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


class Producte(models.Model):
    name = models.CharField(max_length=64)
    delivery_date = models.DateField(null=True,blank=True,help_text="Seleccionar la fecha de salida")
    level_agreement = models.ForeignKey(Level_Agreement,related_name='te',on_delete=models.PROTECT,default='0')
    client = models.ForeignKey(Client, related_name='es_de', on_delete=models.PROTECT, default='0')

    def __str__(self):
        return '%s ( %s - %s )' % (self.name,self.delivery_date, self.client)


class Sala (models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return '%s ' % (self.name)


class Container (models.Model):
    producte = models.ForeignKey(Producte,related_name='conte', on_delete=models.PROTECT)
    dimensio_c = models.ForeignKey(Dimensio,related_name='te',on_delete=models.PROTECT)
    sala = models.ForeignKey(Sala, related_name='descarrega_a', on_delete=models.PROTECT)

    def __str__(self):
        return '%s ( %s )' % (self.producte,self.dimensio_c)


class Ubicacio (models.Model):
    pasillo = models.IntegerField()
    prestatge = models.IntegerField()
    hueco = models.IntegerField()
    sala = models.ForeignKey(Sala,related_name='esta',on_delete=models.PROTECT)
    dimensio = models.ForeignKey(Dimensio, related_name='capacitat', on_delete=models.PROTECT)

    def __str__(self):
        return 'Pas:%sPres:%sH:%s-%s ' % (self.pasillo,self.prestatge,self.hueco,self.sala)