from django.shortcuts import render
from .forms import AnalisisImagenForm
from .models import AnalisisImagen, Paciente
from timeit import default_timer
from django.core import serializers
from django.db.models import Q

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

        if (not json["nombres"]):
        
            # Buscamos en la tabla de paciente
            paciente = Paciente.objects.filter(dni=dni).exists();

            if paciente:
                paciente = Paciente.objects.get(dni=dni)
                
                json = {"dni": dni, "nombre": (paciente.apellidoPaterno + paciente.apellidoMaterno + paciente.nombres),"nombres": paciente.nombres, "apellidoMaterno": paciente.apellidoMaterno, "apellidoPaterno": paciente.apellidoPaterno}
                
                data["bool"]        = True;
                data["resultado"]   = json;
                data["consumo"]     = "BASE DE DATOS";
            else :
                data["bool"]        = False;
                data["resultado"]   = "Persona no pudo ser encontrada";
            
        else:

            # Registramos el paciente
            paciente = Paciente.objects.filter(dni=dni).exists();
            if not paciente:
                paciente = Paciente(dni = dni, nombres = json["nombres"], apellidoMaterno = json["apellidoMaterno"], apellidoPaterno = json["apellidoPaterno"])
                paciente.save()
        
            data["bool"]        = True;
            data["resultado"]   = json;
            data["consumo"]     = "API";
        
        return JsonResponse({"data": data}) 
    
    except:
    
        data = {}
        dni = request.POST["dni"]
        
        # Buscamos en la tabla de paciente
        paciente = Paciente.objects.filter(dni=dni).exists();
        if paciente:
            paciente = Paciente.objects.get(dni=dni)
            
            json = {"dni": dni, "nombre": (paciente.apellidoPaterno + paciente.apellidoMaterno + paciente.nombres),"nombres": paciente.nombres, "apellidoMaterno": paciente.apellidoMaterno, "apellidoPaterno": paciente.apellidoPaterno}
            
            data["bool"]        = True;
            data["resultado"]   = json;
            data["consumo"]     = "BASE DE DATOS";
        else :
            data["bool"]        = False;
            data["resultado"]   = "Persona no pudo ser encontrada";

    return JsonResponse({"data": data})
        
def resultado_imagen(request):

    inicio = default_timer()

    # Inicio del algoritmo
    dni = request.POST["dni"];
    nombres = request.POST["nombres"];
    apellidoMaterno = request.POST["apellidoMaterno"];
    apellidoPaterno = request.POST["apellidoPaterno"];
    titulo = request.POST["titulo"];
    descripcion = request.POST["descripcion"];
    imagen = request.FILES["imagen"];


    analisis = AnalisisImagen(
        dni             = dni, 
        nombres         = nombres, 
        apellidoMaterno = apellidoMaterno, 
        apellidoPaterno = apellidoPaterno, 
        titulo          = titulo, 
        descripcion     = descripcion, 
        imagen          = imagen,
    )

    analisis.save()

    # Enviamos el nombre de la imagen a la predicción
    prediccion = realizar_analisis(imagen.name)
    
    # Fin del algoritmo
    fin = default_timer()
    tiempoEstimado = fin - inicio
    tiempoTotal = round(tiempoEstimado, 4)
    
    prediction = prediccion.get("ConCancer")
    
    # Guardamos los datos del resultado
    p = AnalisisImagen.objects.get(id=analisis.id)
    p.resultado = prediction
    p.tiempo = tiempoTotal
    p.save()

    return render(request, "resultado_imagen.html", {"analisis": analisis, "tiempoTotal": tiempoTotal, "prediccion": prediction})

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

def historial_analisis(request):
    
    elemento = request.POST.get('elemento', False)
    opcion = request.POST.get('opcion', False)

    if(opcion):
       
       elemento = elemento.upper()

       match opcion:
        case "":
            analisis = AnalisisImagen.objects.filter(Q(dni__startswith=elemento) | Q(nombres__startswith=elemento) | Q(apellidoMaterno__startswith=elemento) | Q(apellidoPaterno__startswith=elemento)).order_by('-id').values()
        case "dni":
            analisis = AnalisisImagen.objects.filter(dni__startswith=elemento).order_by('-id').values()
        case "nombres":
            analisis = AnalisisImagen.objects.filter(nombres__startswith=elemento).order_by('-id').values()
        case "apellidoMaterno":
            analisis = AnalisisImagen.objects.filter(apellidoMaterno__startswith=elemento).order_by('-id').values()
        case "apellidoPaterno":
            analisis = AnalisisImagen.objects.filter(apellidoPaterno__startswith=elemento).order_by('-id').values()
        case default:
            analisis = AnalisisImagen.objects.filter(Q(dni__startswith=elemento) | Q(nombres__startswith=elemento) | Q(apellidoMaterno__startswith=elemento) | Q(apellidoPaterno__startswith=elemento)).order_by('-id').values()

    else:
        analisis = AnalisisImagen.objects.all().order_by('-id')
    
    if(not elemento):
       elemento = ""

    return render(request, "historial_analisis.html", {"analisis": analisis, "opcion": opcion, "elemento": elemento})

def pacientes(request):
    
    elemento = request.POST.get('elemento', False)
    opcion = request.POST.get('opcion', False)

    if(opcion):
       
       elemento = elemento.upper()

       match opcion:
        case "":
            pacientes = Paciente.objects.filter(Q(dni__startswith=elemento) | Q(nombres__startswith=elemento) | Q(apellidoMaterno__startswith=elemento) | Q(apellidoPaterno__startswith=elemento)).order_by('-id').values()
        case "dni":
            pacientes = Paciente.objects.filter(dni__startswith=elemento).order_by('-id').values()
        case "nombres":
            pacientes = Paciente.objects.filter(nombres__startswith=elemento).order_by('-id').values()
        case "apellidoMaterno":
            pacientes = Paciente.objects.filter(apellidoMaterno__startswith=elemento).order_by('-id').values()
        case "apellidoPaterno":
            pacientes = Paciente.objects.filter(apellidoPaterno__startswith=elemento).order_by('-id').values()
        case default:
            pacientes = Paciente.objects.filter(Q(dni__startswith=elemento) | Q(nombres__startswith=elemento) | Q(apellidoMaterno__startswith=elemento) | Q(apellidoPaterno__startswith=elemento)).order_by('-id').values()

    else:
        pacientes = Paciente.objects.all().order_by('-id')
    
    if(not elemento):
       elemento = ""

    return render(request, "pacientes.html", {"pacientes": pacientes, "opcion": opcion, "elemento": elemento})