from django.db import models

# Create your models here.

class Manifest(models.Model):

    date = models.DateField(null=True,blank=True,help_text="Seleccione la fecha de entrada")
    reference = models.CharField(max_length = 11)
    fromm = models.ForeignKey('Address',on_delete=models.SET_DEFAULT,default=1)
    to = models.ForeignKey('Address',on_delete=models.SET_DEFAULT,default=1)


    def __str__(self):
        return '%s' % self.reference


class Address(models.Model):
    address = models.CharField(max_length=64, help_text="Inserte la direccion")

    postal_code = models.CharField(max_length=5, help_text="Inserte el codigo postal")

    def __str__(self):
        return 'ZIP: %s - Addrress: %s' % (self.postal_code, self.address)


class Producte(models.Model):
    name = models.CharField()
    delivery_date = models.DateField()


class Container (models.Model):
    producte = models.ManyToManyField(Producte,related_name='es diposita amb')




