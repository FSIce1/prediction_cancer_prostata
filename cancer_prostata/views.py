from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, "login.html", {})

def analisis_imagen(request):
    return render(request, "analisis_imagen.html", {})

def resultado_imagen(request):
    return render(request, "resultado_imagen.html", {})

def resultado_imagen_top(request):
    return render(request, "resultado_imagen_top.html", {})