from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from PyQt5.QtCore import Qt



# Configura los numero float de tbtabla y les da formato de moneda al visualizarse.
class CurrencyDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        try:
            # Convierte el valor a un formato de moneda
            return locale.toCurrencyString(float(value))
        except ValueError:
            # Si no se puede convertir a un formato de moneda, devuelve el valor original
            return value  
    
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  

# Recibe parametros para introducir correspondientes datos a la base de datos.  
def insertar_nuevo_empleados(Nombre, Num_banca, Salario):
    
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

# Recibe parametros para introducir correspondientes datos a la base de datos.       
def insertar_nuevo_faltante(Fecha, Nombre, Num_banca, Abono, Faltante):
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO faltantes (fecha ,nombre, banca, abono, faltante) VALUES (?, ?, ?, ?, ?)", (Fecha, Nombre, Num_banca, Abono, Faltante))
        conn.commit()

        # Cerrar la conexión
        conn.close()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------           
# Función que muestra los datos de los empleados en QTableView del FrmDatos    
def mostrar_datos_de_empleados(tbtabla):
    
    currency_delegate = CurrencyDelegate()
        
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("empleados")
    
    # Establecer el orden en orden ascendente
    model.setSort(0, Qt.AscendingOrder) # type: ignore
    model.select()
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
    # Le da formato moneda a la columna con el indice 2.
    tbtabla.setItemDelegateForColumn(2, currency_delegate)
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Utilisa un query para mostrar datos segun la consulta, esto no modifican los datos solo los muestra.
def mostrar_datos_totales_por_empleados(tbtabla):
    
    
    
    query = QSqlQuery()
    query.exec_("SELECT e.NOMBRE,\
       COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_FALTANTES,\
       COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_ABONOS,\
       e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0)\
       + COALESCE ((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS SALARIO_NETO FROM empleados e")

   
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    
    model.setQuery(query)   
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
                   
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
