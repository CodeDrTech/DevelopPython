class Config:
    SECRET_KEY = 'tu_clave_secreta'  # Cambia esto por una clave segura
    DEBUG = True  # Modo de depuración (cambiar a False en producción)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/data_web.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False