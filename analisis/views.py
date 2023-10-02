from django.shortcuts import render
from .forms import AnalisisImagenForm
from .models import AnalisisImagen

def analisis_imagen(request):
    form = AnalisisImagenForm()
    return render(request, "analisis_imagen.html", {"form": form})
        
def resultado_imagen(request):

    titulo = request.POST["titulo"];
    descripcion = request.POST["descripcion"];
    imagen = request.FILES["imagen"];

    analisis = AnalisisImagen(titulo = titulo, descripcion = descripcion, imagen = imagen)
    analisis.save()

    return render(request, "resultado_imagen.html", {"analisis": analisis})