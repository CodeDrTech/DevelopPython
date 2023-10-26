"SELECT\
                                co.idcotizacion as 'ID',\
                                UPPER(FORMAT(co.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dc.descuento as 'DESCUENTO %',\
                                co.itbis as 'IMPUESTOS %',\
                                co.serie as 'NO. COTIZACION',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dc.precio_venta), 'C', 'en-US') as 'TOTAL',\
                                co.comentario as 'COMENTARIO'\
                            FROM cotizacion co\
                            INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                            INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                            INNER JOIN empleado em ON co.idempleado = em.idempleado\
                            GROUP BY co.idcotizacion, co.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dc.descuento, co.itbis, co.serie, em.nombre, co.comentario;"