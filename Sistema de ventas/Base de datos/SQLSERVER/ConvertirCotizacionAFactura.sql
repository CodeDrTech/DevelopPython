USE [Ventas]
GO

/****** Object:  StoredProcedure [dbo].[ConvertirCotizacionAFactura]    Script Date: 10/26/2023 1:44:43 PM *****/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[ConvertirCotizacionAFactura]
    @idcotizacion INT
AS
BEGIN
    -- Variables locales
    DECLARE @nueva_serie NVARCHAR(MAX);
    DECLARE @idventa INT;
    DECLARE @comentario_venta NVARCHAR(MAX);

    -- Obtener la última serie de ventas
    SELECT TOP 1 @nueva_serie = serie
    FROM venta
    ORDER BY idventa DESC;

    -- Establecer el próximo número de serie
    IF @nueva_serie IS NOT NULL
    BEGIN
        SET @nueva_serie = 'VENT' + RIGHT('00000' + CAST(CAST(RIGHT(@nueva_serie, LEN(@nueva_serie) - 4) AS INT) + 1 AS NVARCHAR), 5);
    END
    ELSE
    BEGIN
        SET @nueva_serie = 'VENT00001';
    END;

    -- Obtener la serie de la cotización que se convierte en venta
    SELECT @comentario_venta = 'COTIZACION NO. ' + serie
    FROM cotizacion
    WHERE idcotizacion = @idcotizacion;

    -- Insertar una nueva venta con el tipo_comprobante y serie actualizados
    INSERT INTO venta (idcliente, idempleado, fecha, tipo_comprobante, serie, itbis, comentario)
    SELECT idcliente, idempleado, GETDATE(), 'FACTURA', @nueva_serie, itbis, @comentario_venta
    FROM cotizacion
    WHERE idcotizacion = @idcotizacion;

    -- Obtener el ID de la venta recién insertada
    SET @idventa = SCOPE_IDENTITY();

    -- Insertar los detalles de la venta
    INSERT INTO detalle_venta (idventa, idarticulo, cantidad, precio_venta, descuento)
    SELECT @idventa, idarticulo, cantidad, precio_venta, descuento
    FROM detalle_cotizacion
    WHERE idcotizacion = @idcotizacion;
END;
GO


