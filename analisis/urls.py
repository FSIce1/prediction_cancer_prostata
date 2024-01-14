from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name="inicio"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('analisis_imagen/', views.analisis_imagen, name="analisis_imagen"),
    path('create_user/', views.create_user, name="create_user"),
    path('buscar_por_dni/', views.buscar_por_dni, name="buscar_por_dni"),
    path('resultado_imagen/', views.resultado_imagen, name="resultado_imagen"),
    path('historial_analisis/', views.historial_analisis, name="historial_analisis"),
    path('pacientes/', views.pacientes, name="pacientes"),
]