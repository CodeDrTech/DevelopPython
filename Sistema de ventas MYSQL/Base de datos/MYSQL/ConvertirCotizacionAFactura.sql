DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConvertirCotizacionAFactura`(
    IN idcotizacion INT
)
BEGIN
    -- Variables locales
    DECLARE nueva_serie VARCHAR(255);
    DECLARE idventa INT;
    DECLARE comentario_venta VARCHAR(255);

    -- Obtener la última serie de ventas
    SELECT serie INTO nueva_serie
    FROM venta
    ORDER BY idventa DESC
    LIMIT 1;

    -- Establecer el próximo número de serie
    IF nueva_serie IS NOT NULL THEN
        SET nueva_serie = CONCAT('FACT', LPAD(RIGHT(nueva_serie, LENGTH(nueva_serie) - 4) + 1, 5, '0'));
    ELSE
        SET nueva_serie = 'FACT00001';
    END IF;

    -- Obtener la serie de la cotización que se convierte en venta
    SELECT CONCAT('COTIZACION NO. ', serie) INTO comentario_venta
    FROM cotizacion
    WHERE idcotizacion = idcotizacion;

    -- Actualizar el campo "disponible" en la tabla "stock" restando la cantidad de la tabla "detalle_cotizacion"
    UPDATE stock s
    JOIN detalle_cotizacion dc ON s.idarticulo = dc.idarticulo
    SET s.disponible = s.disponible - dc.cantidad
    WHERE dc.idcotizacion = idcotizacion;

    -- Insertar una nueva venta con el tipo_comprobante y serie actualizados
    INSERT INTO venta (idcliente, idempleado, fecha, tipo_comprobante, serie, itbis, comentario)
    SELECT idcliente, idempleado, NOW(), 'FACTURA', nueva_serie, itbis, comentario_venta
    FROM cotizacion
    WHERE idcotizacion = idcotizacion;

    -- Obtener el ID de la venta recién insertada
    SET idventa = LAST_INSERT_ID();

    -- Insertar los detalles de la venta
    INSERT INTO detalle_venta (idventa, idarticulo, cantidad, precio_venta, descuento)
    SELECT idventa, idarticulo, cantidad, precio_venta, descuento
    FROM detalle_cotizacion
    WHERE idcotizacion = idcotizacion;
END$$
DELIMITER ;
