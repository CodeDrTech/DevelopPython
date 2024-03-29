USE [Ventas]
GO

CREATE PROCEDURE RevertirDetalleVenta @iddetalle_venta INT AS
BEGIN
    -- Declara las variables
    DECLARE @idventa INT, @idarticulo INT, @cantidad INT

    -- Obtén el detalle de venta
    SELECT @idventa = idventa, @idarticulo = idarticulo, @cantidad = cantidad
    FROM detalle_venta
    WHERE iddetalle_venta = @iddetalle_venta

    -- Aumenta la cantidad de stock
    UPDATE stock
    SET disponible = disponible + @cantidad
    WHERE idarticulo = @idarticulo

    -- Elimina el detalle de venta
    DELETE FROM detalle_venta
    WHERE iddetalle_venta = @iddetalle_venta

    -- Verifica si la venta ya no tiene más detalles
    IF NOT EXISTS (SELECT 1 FROM detalle_venta WHERE idventa = @idventa)
    BEGIN
        -- Actualiza el comentario de la venta
        UPDATE venta
        SET comentario = 'SIN ARTICULOS'
        WHERE idventa = @idventa
    END
END