from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')

# Importar rutas después de inicializar la aplicación para evitar importaciones circulares
from app import routes