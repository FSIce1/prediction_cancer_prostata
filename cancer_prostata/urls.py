from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', views.login, name="login"),
    path('analisis_imagen/', views.analisis_imagen, name="analisis_imagen"),
]
