from django.shortcuts import render
from .forms import AnalisisImagenForm
from .models import AnalisisImagen
from timeit import default_timer

# Modelo
import numpy as np
import tensorflow as tf
from PIL import Image

# Api - Reniec
from urllib.request import urlopen
from django.http import JsonResponse 
# import json
import requests
from django.views.decorators.csrf import csrf_exempt

url = "https://api.apis.net.pe/v1/dni?numero="

# Funciones
def analisis_imagen(request):
    form = AnalisisImagenForm()
    return render(request, "analisis_imagen.html", {"form": form})

@csrf_exempt
def buscar_por_dni(request):

    try:
        
        dni = request.POST["dni"]  
        
        response = requests.get(url+dni, headers={})
        json = response.json()
        
        data = {}
        data["bool"] = True;
        data["resultado"] = json;

        return JsonResponse({"data": data}) 
    
    except:
    
        data = {}
        data["bool"] = False;
        data["resultado"] = "Persona no pudo ser encontrada";

        return JsonResponse({"data": data}) 
    
        
def resultado_imagen(request):

    inicio = default_timer()

    # Inicio del algoritmo
    titulo = request.POST["titulo"];
    descripcion = request.POST["descripcion"];
    imagen = request.FILES["imagen"];


    analisis = AnalisisImagen(titulo = titulo, descripcion = descripcion, imagen = imagen)
    analisis.save()

    # Enviamos el nombre de la imagen a la predicción
    prediccion = realizar_analisis(imagen.name)
    
    # Fin del algoritmo
    fin = default_timer()
    tiempoEstimado = fin - inicio
    tiempoTotal = round(tiempoEstimado, 4)
    
    return render(request, "resultado_imagen.html", {"analisis": analisis, "tiempoTotal": tiempoTotal, "prediccion": prediccion})

def realizar_analisis(url_imagen = ""):
    
    # archi1=open("analisis/utils/logs.txt","w") 
    # archi1.write(url_imagen) 
    # archi1.close()

    # PARTE 1
    BREED_FILE = "analisis/utils/breeds.txt"
    MODEL_FILE = "analisis/models/modelo_vgg16_512px.h5"
    IMG_SIZE = 512

    labels = []
    with open(BREED_FILE, "r") as f:
        for line in f:
            labels.append(line.strip())

    loaded_model = tf.keras.models.load_model(MODEL_FILE)
    loaded_model.summary()

    # image_file = "files/imagenes/pruebas/imagen_de_prueba.jpg"
    image_file = "files/imagenes/"+url_imagen

    n_top = 2

    img = np.array(Image.open(image_file).resize((IMG_SIZE,IMG_SIZE)), dtype=np.float32)
    pred = loaded_model.predict(img.reshape(-1, IMG_SIZE, IMG_SIZE, 3))

    top_labels = {}
    if len(labels) >= n_top:
        top_labels_ids = np.flip(np.argsort(pred, axis=1)[0, -n_top:])
        for label_id in top_labels_ids:
            top_labels[labels[label_id]] = pred[0,label_id].item()

    return top_labels