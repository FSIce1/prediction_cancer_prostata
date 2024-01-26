from django.shortcuts import render, redirect
from .forms import AnalisisImagenForm
from .models import AnalisisImagen, UsuarioLogueo, Paciente, Logs
from timeit import default_timer
from django.core import serializers
from django.db.models import Q
from decimal import Decimal, getcontext
from django.contrib.auth import authenticate, login

# Firebase
import firebase_admin
from firebase_admin import credentials, auth, db

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

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
import textwrap

url = "https://api.apis.net.pe/v1/dni?numero="

# Funciones

def create_user(request):
    
    try:
    
        email = request.POST["email"];
        password = request.POST["password"];
            
        # Registramos el usuario
        usuario = UsuarioLogueo.objects.filter(email=email).exists();
        
        if not usuario:
            usuario = UsuarioLogueo(email = email, password = password)
            usuario.save()
        
        if not firebase_admin._apps:
            firebase_sdk = credentials.Certificate('cancer_prostata/tesis-prostata-firebase-adminsdk-cjra8-fa2078f5be.json')
            firebase_admin.initialize_app(firebase_sdk)

        user = auth.create_user(email = email, password = password)

        return render(request, "login.html", {"message": "Usuario creado correctamente"})
    
    except:
    
        return render(request, "login.html", {"message": "Usuario no pudo ser creado"})

def inicio(request):

    if not firebase_admin._apps:
        firebase_sdk = credentials.Certificate('cancer_prostata/tesis-prostata-firebase-adminsdk-cjra8-fa2078f5be.json')
        firebase_admin.initialize_app(firebase_sdk)

    email = request.POST["email"];
    password = request.POST["password"];

    try:
        
        boolUser = UsuarioLogueo.objects.filter(email=email).exists();

        if boolUser:

            usuario = UsuarioLogueo.objects.get(email=email)

            if(usuario.password == password):
            
                usuario_firebase = auth.get_user_by_email(email)
            
                # Obtener el UID del usuario
                uid_usuario = usuario_firebase.uid

                uid = uid_usuario
                usuario_firebase = auth.get_user(uid)
                usuario_django = authenticate(request, uid=usuario_firebase.uid)

                if usuario_django is not None:
                    login(request, usuario_django)
                
                datos = {
                    'uid': usuario_firebase.uid,
                    'email': usuario_firebase.email,
                }

                usuario_firebase = auth.get_user(uid)
                
                request.session['dataUser'] = datos

                form = AnalisisImagenForm()
                return render(request, "analisis_imagen.html", {"form": form, "modo": "analisis", "email": usuario_firebase.email})
            
            else:

                return render(request, "login.html", {"message": "La contraseña es incorrecta"})
        
        else:

            return render(request, "login.html", {"message": "El usuario no existe"})

    except Exception as e:

        return render(request, "login.html", {"message": e})

def analisis_imagen(request):

    dataUser = request.session.get('dataUser', None)

    form = AnalisisImagenForm()
    return render(request, "analisis_imagen.html", {"form": form, "modo": "analisis", "email": dataUser["email"]})    
    
def cerrar_sesion(request):

    dataUser = request.session.get('dataUser', None)

    user_id = dataUser["uid"]
    auth.revoke_refresh_tokens(user_id)
    
    return render(request, 'login.html')

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

    try:

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

        results = logicLabel(prediction)
        
        # Guardamos los datos del resultado
        p = AnalisisImagen.objects.get(id=analisis.id)
        p.resultado = prediction
        p.tiempo = tiempoTotal
        p.modo = results["label"]
        p.prediccion = results["prediction"]
        p.save()
        
        dataUser = request.session.get('dataUser', None)

    except:

        log = Logs(
            funcion     = "resultado_imagen", 
            resultado   = "Problema al guardar el análisis",
        )

        log.save()

    return render(request, "resultado_imagen.html", {"analisis": analisis, "modo": "analisis", "tiempoTotal": tiempoTotal, "prediccion": prediction, "results": results, "label": results["label"], "prediction": results["prediction"], "email": dataUser["email"], "id": p.id})

def logicLabel(prediction):

    prediction = float(prediction) * float(100);

    if(prediction > 80):
        return {"label": "Sin Cáncer", "prediction": prediction}
    else:
        factor_multiplicacion = Decimal(100) - Decimal(prediction)
        return {"label": "Con Cáncer", "prediction": factor_multiplicacion}

def realizar_analisis(url_imagen = ""):
    
    try:

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

        image_file = "files/imagenes/"+url_imagen

        n_top = 2

        img = np.array(Image.open(image_file).resize((IMG_SIZE,IMG_SIZE)), dtype=np.float32)
        pred = loaded_model.predict(img.reshape(-1, IMG_SIZE, IMG_SIZE, 3))

        top_labels = {}
        if len(labels) >= n_top:
            top_labels_ids = np.flip(np.argsort(pred, axis=1)[0, -n_top:])
            for label_id in top_labels_ids:
                top_labels[labels[label_id]] = pred[0,label_id].item()

    except:
    
        log = Logs(
            funcion     = "realizar_analisis", 
            resultado   = "Problema al hacer la predicción de la imagen",
        )

        log.save()

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

    dataUser = request.session.get('dataUser', None)
       
    return render(request, "historial_analisis.html", {"analisis": analisis, "opcion": opcion, "elemento": elemento, "modo": "historial", "email": dataUser["email"]})

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

    dataUser = request.session.get('dataUser', None)

    return render(request, "pacientes.html", {"pacientes": pacientes, "opcion": opcion, "elemento": elemento, "modo": "pacientes", "email": dataUser["email"]})

def generate_pdf(request):

    identificador = request.POST["id"] 
    analisis = AnalisisImagen.objects.filter(id=identificador).exists();

    if analisis:

        analisis = AnalisisImagen.objects.get(id=identificador)
    
        # Crea un objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="reporte_final.pdf"; inline'

        pdf = canvas.Canvas(response, pagesize=letter)

        # text_color = Color(0.8, 0.8, 0.8)  # Gris claro

        # TÍTULO
        title = "REPORTE FINAL"
        width, height = letter

        text_width = pdf.stringWidth(title, "Helvetica-Bold", 16)
        x = (width - text_width) / 2
        y = 750
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, title)

        x = 100
        y-=50
        # TODO: INFORMACIÓN DEL PACIENTE
        pdf.setFillColorRGB(0, 0, 1)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x, y, 'Información del paciente')
        pdf.setFillColorRGB(0, 0, 0)
        
        # DNI
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "DNI:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.dni)

        # NOMBRES
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Nombres:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.nombres)

        # APELLIDO PATERNO
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Apellido Paterno:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.apellidoPaterno)

        # APELLIDO MATERNO
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Apellido Materno:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.apellidoMaterno)


        # TODO: INFORMACIÓN DEL RESULTADO
        y-=40
        pdf.setFillColorRGB(0, 0, 1)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x, y, 'Información del resultado')
        pdf.setFillColorRGB(0, 0, 0)
        
        # TÍTULO
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Título:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.titulo)

        # DESCRIPCIÓN
        y-=30
        description = analisis.descripcion; #"kasdjskajdoikasjdkjaskodjaskdjsakdhkasghdjasgdasgvdjasgjdgasjdgashjdgasjhdgsajhgdjashgdjashgdasjhgdasjdgasjhdgasjdgasjdgasjgdasjhdgasjgdasjgdasjhdgasjhdgasjdgasjdgsajhdgasjdhgasjdhasgdjhsagdjhsagdhjasgewqyueuisgaydasjdbashgdfsahjdbsadhrte cvendfidosfjdsnfsdbf lñsdiusñfdsn´sdfklsdjnfká"
        long_description = 80
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, analisis.descripcion)
        pdf.setFont("Helvetica", 12)
        y-=15
        parts = textwrap.wrap(description, long_description)
        for part in parts:
            pdf.drawString(x, y, part)
            y -= 15

        
        # TODO: RESUMEN FINAL
        y-=30
        pdf.setFillColorRGB(0, 0, 1)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x, y, 'Resumen Final')
        pdf.setFillColorRGB(0, 0, 0)

        y-=150
        image_path = "files/"+str(analisis.imagen) 
        pdf.drawImage(image_path, ((width - 130) / 2), y, width=130, height=130)
        
        # Tiempo de análisis
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Tiempo de análisis:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.tiempo + " seg")

        # Resultado final
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Resultado Final:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.modo)

        # Porcentaje
        y-=30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Porcentaje:")
        y-=15
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y, analisis.prediccion)

        y-=30
        pdf.line(100, y, 700, y)

        pdf.showPage()
        pdf.save()

        return response
    
    else:

        dataUser = request.session.get('dataUser', None)

        form = AnalisisImagenForm()

        return render(request, "analisis_imagen.html", {"form": form, "modo": "analisis", "email": dataUser["email"]})    
