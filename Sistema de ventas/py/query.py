SELECT dc.iddetalle_cotizacion as 'ID DETALLE',\
                        dc.idcotizacion as 'ID COTIZACION',\
                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                        ar.nombre as 'ARTICULO',\
                        FORMAT(dc.precio_venta, 'C', 'en-US') as 'PRECIO',\
                        dc.cantidad as 'CANTIDAD',\
                        dc.descuento as 'DESCUENTO %',\
                        co.itbis as 'IMPUESTOS',\
                        co.serie as 'NO. COTIZACION',\
                        em.nombre as 'VENDEDOR'\
                    FROM cotizacion co\
                    INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                    INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                    INNER JOIN articulo ar ON dc.idarticulo = ar.idarticulo\
                    INNER JOIN empleado em ON co.idempleado = em.idempleado\
                    WHERE dc.idcotizacion = {idcotizacion};
