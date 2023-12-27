import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db

# Se cargan las credenciales del firebase
firebase_sdk = credentials.Certificate('cancer_prostata/tesis-prostata-firebase-adminsdk-cjra8-fa2078f5be.json')

# Inicializamos la conexión a la base de datos en tiempo real de firebase
# firebase_admin.initialize_app(firebase_sdk, {'databaseURL': 'https://tesis-prostata-default-rtdb.firebaseio.com/'})
firebase_admin.initialize_app(firebase_sdk)

user = auth.create_user(email = "luisfelipesiesquen2@gmial.com", password = "123456")

# ref = db.reference('/Productos')
# ref.push({'tipo':"Prueba 1", "marca": "Prueba 1", "modelo": "Prueba 1", "sistema": "Prueba 1"})
