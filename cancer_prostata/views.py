from django.shortcuts import render
from django.http import HttpResponse
from .forms import AnalisisImagenForm

def login(request):
    return render(request, "login.html", {})

def analisis_imagen(request):
    form = AnalisisImagenForm()
    return render(request, "analisis_imagen.html", {"form": form})
        
def resultado_imagen(request):
    
    form = AnalisisImagenForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()

    titulo = request.POST["titulo"];
    descripcion = request.POST["descripcion"];
    
    return render(request, "resultado_imagen.html", {"titulo": titulo, "descripcion": descripcion})