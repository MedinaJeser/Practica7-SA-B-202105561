import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de conexión desde las variables de entorno
MONGO_URL = os.getenv("DATABASE_URL")

# Crear la conexión a MongoDB
client = MongoClient(MONGO_URL)

# Seleccionar la base de datos y la colección
database = client["enrollments_ms"]
enrollment_collection = database["enrollments"]
