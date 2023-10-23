def quitar_detalle_cotizacion(id_detalle_cotizacion):
    try:
        conn = conectar_db()  # Utiliza tu función de conexión a la base de datos
        cursor = conn.cursor()

        # Obtener el idcotizacion desde el detalle
        cursor.execute("SELECT iddetalle_cotizacion, idcotizacion FROM detalle_cotizacion WHERE iddetalle_cotizacion = ?", (id_detalle_cotizacion,))
        detalle = cursor.fetchone()

        if detalle:
            iddetalle_cotizacion, idcotizacion = detalle

            # Eliminar el detalle de cotizacion
            cursor.execute("DELETE FROM detalle_cotizacion WHERE iddetalle_cotizacion = ?", (iddetalle_cotizacion,))

            # Comprobar si la cotizacion ya no tiene más detalles
            cursor.execute("SELECT COUNT(*) FROM detalle_cotizacion WHERE idcotizacion = ?", (idcotizacion,))
            num_detalles = cursor.fetchone()[0]

            if num_detalles == 0:

                # Agregar un detalle de cotización genérico
                cursor.execute("INSERT INTO detalle_cotizacion (idcotizacion, idarticulo, cantidad) VALUES (?, 1, 0)", (idcotizacion,))

                # Actualizar el comentario en la cotización
                cursor.execute("UPDATE cotizacion SET comentario = 'COTIZACION ANULADA' WHERE idcotizacion = ?", (idcotizacion,))

            conn.commit()
        else:
            mensaje_error = QMessageBox()
            mensaje_error.setWindowTitle("Error")
            mensaje_error.setText("Detalle de cotizacion no encontrado.")
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.exec()

        conn.close()
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al anular el ingreso: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
