from database import connect_to_db

connection = connect_to_db()
if connection:
    cursor = connection.cursor()
    cursor.execute("""SELECT u.nombres AS Nombre,
                             u.apellidos AS Apellido,
                             u.cedula AS Cedula,
                             u.numeroEmpleado AS Empleado,
                             e.marca AS Marca,
                             e.modelo AS Modelo,
                             e.condicion AS Condicion,
                             c.numeroContrato AS NumeroContrato,
                             FORMAT(c.fecha, 'dd/MM/yyyy') AS Fecha
                      FROM Usuario u
                      INNER JOIN Equipo e ON u.idUsuario = e.idUsuario
                      INNER JOIN Contrato c ON u.idUsuario = c.idUsuario AND e.idEquipo = c.idEquipo
                      ORDER BY c.fecha DESC""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    connection.close()
