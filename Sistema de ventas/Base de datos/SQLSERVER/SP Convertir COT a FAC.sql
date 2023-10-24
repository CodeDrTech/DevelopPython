  CREATE PROCEDURE ConvertirCotizacionAFactura
    @idcotizacion INT
AS
BEGIN
    DECLARE @nueva_serie NVARCHAR(MAX);
    
    -- Obtener el ultimo numero de serie de ventas
    SELECT @nueva_serie = 'VENT' + RIGHT('00000' + CAST(ISNULL(MAX(CAST(RIGHT(serie, LEN(serie) - 4) AS INT)), 0) + 1 AS NVARCHAR(5)), 5)
    FROM venta;

    -- Insertar en la tabla de ventas
    INSERT INTO venta (idcliente, idempleado, fecha, tipo_comprobante, serie, itbis)
    SELECT idcliente, idempleado, GETDATE(), 'FACTURA', @nueva_serie, itbis
    FROM cotizacion
    WHERE idcotizacion = @idcotizacion;

    -- Obtener el ID de la venta recien insertada
    DECLARE @idventa INT;
    SELECT @idventa = SCOPE_IDENTITY();

    -- Insertar detalles de la venta
    INSERT INTO detalle_venta (idventa, idarticulo, cantidad, precio_venta, descuento)
    SELECT @idventa, idarticulo, cantidad, precio_venta, descuento
    FROM detalle_cotizacion
    WHERE idcotizacion = @idcotizacion;
END


--EXEC ConvertirCotizacionAFactura @idcotizacion = 1; -- Reemplaza 1 con el ID de la cotizacion que deseas convertir
