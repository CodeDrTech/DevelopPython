CREATE PROCEDURE AnularDetalleCotizacion
    @iddetalle_cotizacion INT
AS
BEGIN
    -- Declarar variables
    DECLARE @idcotizacion INT;

    -- Obtener el idcotizacion desde el detalle
    SELECT @idcotizacion = idcotizacion
    FROM detalle_cotizacion
    WHERE iddetalle_cotizacion = @iddetalle_cotizacion;

    -- Eliminar el detalle de cotización
    DELETE FROM detalle_cotizacion
    WHERE iddetalle_cotizacion = @iddetalle_cotizacion;

    -- Comprobar si la cotización ya no tiene más detalles
    IF NOT EXISTS (SELECT 1 FROM detalle_cotizacion WHERE idcotizacion = @idcotizacion)
    BEGIN
        -- Agregar un detalle de cotización genérico
        INSERT INTO detalle_cotizacion (idcotizacion, idarticulo, cantidad, precio_venta, descuento)
        VALUES (@idcotizacion, 1, 0, 0, 0);

        -- Actualizar el comentario en la cotización
        UPDATE cotizacion
        SET comentario = 'COTIZACIÓN ANULADA'
        WHERE idcotizacion = @idcotizacion;
    END;
END;
