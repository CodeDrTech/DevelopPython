import sqlite3
import random
import string
import io
from PIL import Image, ImageDraw, ImageFont
from Conexion_db import conectar_db


from PIL import Image, ImageDraw

def generate_image_blob(description):
    """Genera un BLOB de imagen a partir de la descripción de texto."""

    # Crea una imagen en blanco de 100x100 píxeles.
    image = Image.new('RGB', (200, 200), color='white')
    
    # Crea un objeto de dibujo en la imagen.
    draw = ImageDraw.Draw(image)
    
    # Configura la fuente y tamaño para el texto.
    font = ImageFont.load_default()  # Puedes ajustar la fuente y el tamaño según tus preferencias.

    # Dibuja el texto en la imagen.
    draw.text((10, 10), description, fill='black', font=font)
    
    # Convierte la imagen en un objeto BytesIO para obtener los datos binarios.
    image_io = io.BytesIO()
    image.save(image_io, format='PNG')
    
    # Obtiene los datos binarios de la imagen.
    image_data = image_io.getvalue()

    # Crea un BLOB con los datos de la imagen.
    blob = io.BytesIO(image_data)
    blob.seek(0)
    return blob



def update_table(conn, table_name, column_name, data):
    """Actualiza la tabla con los datos proporcionados."""

    # Obtiene un cursor para la conexión.
    cursor = conn.cursor()

    # Crea una consulta UPDATE.
    query = "UPDATE {} SET {}=? WHERE idarticulo=?".format(table_name, column_name)

    # Ejecuta la consulta para cada registro.
    for idarticulo, description in data:
        blob = generate_image_blob(description)
        
        # Convierte el objeto _io.BytesIO en bytes.
        blob_data = blob.read()

        cursor.execute(query, (blob_data, idarticulo))

    # Realiza los cambios en la base de datos.
    conn.commit()


# Conecta a la base de datos.
conn = conectar_db()

# Obtiene los datos de la tabla.
data = []
for idarticulo, name, description in conn.execute('SELECT idarticulo, nombre, descripcion FROM articulo'):
    data.append((idarticulo, description))

# Actualiza la tabla con los datos generados.
update_table(conn, 'articulo', 'imagen', data)

# Cierra la conexión a la base de datos.
conn.close()
