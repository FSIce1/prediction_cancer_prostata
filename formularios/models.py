from django.db import models

class AnalisisImagen(models.Model):
    titulo = models.CharField(max_length=150, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    imagen = models.ImageField(upload_to="imagenes", null=True)

    def __str__(self):
        return self.titulo