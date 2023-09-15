from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    titulo=models.CharField(max_length=100)
    descripcion= models.TextField(blank=True)
    creada=models.DateTimeField(auto_now_add=True)
    completada_fecha= models.DateTimeField(null=True, blank=True )
    importante=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - para - '+self.user.username
