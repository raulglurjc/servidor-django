from django.db import models
from django.utils import timezone
# Create your models here.
class Database_Users(models.Model):
    username = models.CharField(max_length=64, default="")
    email = models.EmailField(max_length=64, default="")
    password = models.CharField(max_length=64, default="")
    image = models.ImageField(upload_to='Usuario', default="avatar.png", blank=True, null=True)

    def __str__(self):
        return self.username + " " + self.email + " " + self.password





class Alimentador(models.Model):
    tipo_alimentador = models.CharField(max_length=64,default="")
    clave = models.CharField(max_length=64, default="")
    nombre = models.CharField(max_length=64, default="")
    url = models.CharField(max_length=64, default="")
    puntuacion = models.IntegerField(default=0)
    seleccionado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre


class Item(models.Model):
    alimentador = models.ForeignKey(Alimentador, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=64, default="")
    enlace = models.CharField(max_length=64, default="")
    clave = models.CharField(max_length=64, default="")
    media = models.CharField(max_length=64, default="")
    info = models.TextField(blank=False, default="")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    popularidad = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    usuario = models.ForeignKey(Database_Users, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    cuerpo = models.TextField(blank=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)



class Voto(models.Model):

    estado = models.CharField(max_length=64, default="")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Database_Users, on_delete=models.CASCADE)
