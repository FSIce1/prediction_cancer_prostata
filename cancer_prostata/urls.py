from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('analisis_imagen/', views.analisis_imagen, name="analisis_imagen"),
    path('resultado_imagen/', views.resultado_imagen, name="resultado_imagen"),
]
