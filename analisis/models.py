from django.db import models

class AnalisisImagen(models.Model):
    dni = models.CharField(max_length=8, blank=False, null=False, default='')
    nombres = models.CharField(max_length=150, blank=False, null=False, default='')
    apellidoMaterno = models.CharField(max_length=150, blank=False, null=False, default='')
    apellidoPaterno = models.CharField(max_length=150, blank=False, null=False, default='')
    titulo = models.CharField(max_length=150, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    imagen = models.ImageField(upload_to="imagenes", null=True)
    resultado = models.CharField(max_length=150, blank=False, null=True, default='')
    tiempo = models.CharField(max_length=150, blank=False, null=True, default='')

    def __str__(self):
        return self.titulo
    
class Paciente(models.Model):
    dni = models.CharField(max_length=8, blank=False, null=False, default='')
    nombres = models.CharField(max_length=150, blank=False, null=False, default='')
    apellidoMaterno = models.CharField(max_length=150, blank=False, null=False, default='')
    apellidoPaterno = models.CharField(max_length=150, blank=False, null=False, default='')

    def __str__(self):
        return self.dni
    
class Logs(models.Model):
    funcion = models.CharField(max_length=150, blank=False, null=False, default='')
    resultado = models.CharField(max_length=150, blank=False, null=False, default='')

    def __str__(self):
        return self.funcion