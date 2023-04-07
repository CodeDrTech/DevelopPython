import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('C:\\Users\\Jose\\Documents\\Base de datos\\MiniNomina.db')

# Realizar una consulta SELECT
cursor = conn.execute("SELECT * FROM empleados")

# Recorrer los resultados de la consulta
for row in cursor:
    print("nombre:", row[0])
    print("num_banca:", row[1])
    print("salario:", row[2])

# Cerrar la conexión
conn.close()
