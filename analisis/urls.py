from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('analisis_imagen/', views.analisis_imagen, name="analisis_imagen"),
    path('resultado_imagen/', views.resultado_imagen, name="resultado_imagen"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(static.MEDIA_URL, document_root=settings.MEDIA_ROOT)