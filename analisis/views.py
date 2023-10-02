from django.shortcuts import render
from .forms import AnalisisImagenForm
from .models import AnalisisImagen
from timeit import default_timer

def analisis_imagen(request):
    form = AnalisisImagenForm()
    return render(request, "analisis_imagen.html", {"form": form})
        
def resultado_imagen(request):

    inicio = default_timer()

    # Inicio del algoritmo
    titulo = request.POST["titulo"];
    descripcion = request.POST["descripcion"];
    imagen = request.FILES["imagen"];

    analisis = AnalisisImagen(titulo = titulo, descripcion = descripcion, imagen = imagen)
    analisis.save()

    # Fin del algoritmo

    fin = default_timer()
    tiempoEstimado = fin - inicio
    tiempoTotal = round(tiempoEstimado, 4)

    return render(request, "resultado_imagen.html", {"analisis": analisis, "tiempoTotal": tiempoTotal})