CREATE PROCEDURE ConvertirCotizacionAFactura
    @idcotizacion INT
AS
BEGIN
    -- Variables locales
    DECLARE @nueva_serie NVARCHAR(MAX);
    DECLARE @idventa INT;
    DECLARE @comentario_venta NVARCHAR(MAX);

    -- Obtener la �ltima serie de ventas
    SELECT TOP 1 @nueva_serie = serie
    FROM venta
    ORDER BY idventa DESC;

    -- Establecer el pr�ximo n�mero de serie
    IF @nueva_serie IS NOT NULL
    BEGIN
        SET @nueva_serie = 'FACT' + RIGHT('00000' + CAST(CAST(RIGHT(@nueva_serie, LEN(@nueva_serie) - 4) AS INT) + 1 AS NVARCHAR), 5);
    END
    ELSE
    BEGIN
        SET @nueva_serie = 'FACT00001';
    END;

    -- Obtener la serie de la cotizaci�n que se convierte en venta
    SELECT @comentario_venta = 'COTIZACION NO. ' + serie
    FROM cotizacion
    WHERE idcotizacion = @idcotizacion;

    -- Actualizar el campo "disponible" en la tabla "stock" restando la cantidad de la tabla "detalle_cotizacion"
    UPDATE s
    SET s.disponible = s.disponible - dc.cantidad
    FROM stock s
    JOIN detalle_cotizacion dc ON s.idarticulo = dc.idarticulo
    WHERE dc.idcotizacion = @idcotizacion;

    -- Insertar una nueva venta con el tipo_comprobante y serie actualizados
    INSERT INTO venta (idcliente, idempleado, fecha, tipo_comprobante, serie, itbis, comentario)
    SELECT idcliente, idempleado, GETDATE(), 'FACTURA', @nueva_serie, itbis, @comentario_venta
    FROM cotizacion
    WHERE idcotizacion = @idcotizacion;

    -- Obtener el ID de la venta reci�n insertada
    SET @idventa = SCOPE_IDENTITY();

    -- Insertar los detalles de la venta
    INSERT INTO detalle_venta (idventa, idarticulo, cantidad, precio_venta, descuento)
    SELECT @idventa, idarticulo, cantidad, precio_venta, descuento
    FROM detalle_cotizacion
    WHERE idcotizacion = @idcotizacion;
END;
