CREATE PROCEDURE RevertirVenta
    @idventa INT
AS
BEGIN
    -- Cambiar el comentario de la venta a "DEVOLUCIÓN DE VENTA"
    UPDATE venta
    SET comentario = 'DEVOLUCIÓN DE VENTA'
    WHERE idventa = @idventa;

    -- Recuperar los detalles de la venta
    DECLARE @idarticulo INT, @cantidad INT;
    DECLARE cursor_detalle CURSOR FOR 
    SELECT idarticulo, cantidad FROM detalle_venta WHERE idventa = @idventa;

    OPEN cursor_detalle;

    FETCH NEXT FROM cursor_detalle INTO @idarticulo, @cantidad;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Para cada artículo vendido, incrementar la cantidad disponible en la tabla de stock
        UPDATE stock
        SET disponible = disponible + @cantidad
        WHERE idarticulo = @idarticulo;

        FETCH NEXT FROM cursor_detalle INTO @idarticulo, @cantidad;
    END;

    CLOSE cursor_detalle;
    DEALLOCATE cursor_detalle;
END;