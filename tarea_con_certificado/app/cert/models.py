from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class cert(models.Model):
    name=  models.CharField("nombre",max_length=50)
    last_name1 =  models.CharField("apellido1",max_length=20)
    last_name2=models.CharField("apellido2",max_length=20)
    texto=RichTextField() 
    dni=models.CharField("dni",max_length=9,unique=True)
    def __str__(self):
        return self.name +"-"+self.last_name+"-"+str(self.texto)+"-"+str(self.id)



  