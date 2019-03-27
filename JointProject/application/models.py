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
        return 'Postal Code: %s - Addrress: %s' % (self.postal_code, self.address)


class Producte(models.Model):
    name = models.CharField(max_length=64)
    delivery_date = models.DateField(null=True,blank=True,help_text="Seleccionar la fecha de salida")

    def __str__(self):
        return '%s ( %s )' % (self.name,self.delivery_date)

"""""""""""
class Container (models.Model):
    producte = models.ManyToManyField(Producte,related_name='es diposita amb')

"""""""""""



