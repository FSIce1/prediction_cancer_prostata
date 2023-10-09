from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('analisis_imagen/', views.analisis_imagen, name="analisis_imagen"),
    path('buscar_por_dni/', views.buscar_por_dni, name="buscar_por_dni"),
    path('resultado_imagen/', views.resultado_imagen, name="resultado_imagen"),
]