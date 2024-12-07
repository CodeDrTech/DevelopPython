DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `RevertirDetalleVenta`(
    IN iddetalle_venta INT
)
BEGIN
    -- Declara las variables
    DECLARE idventa INT;
    DECLARE idarticulo INT;
    DECLARE cantidad INT;

    -- Obtén el detalle de venta
    SELECT idventa, idarticulo, cantidad INTO idventa, idarticulo, cantidad
    FROM detalle_venta
    WHERE iddetalle_venta = iddetalle_venta;

    -- Aumenta la cantidad de stock
    UPDATE stock
    SET disponible = disponible + cantidad
    WHERE idarticulo = idarticulo;

    -- Elimina el detalle de venta
    DELETE FROM detalle_venta
    WHERE iddetalle_venta = iddetalle_venta;

    -- Verifica si la venta ya no tiene más detalles
    IF NOT EXISTS (SELECT 1 FROM detalle_venta WHERE idventa = idventa) THEN
        -- Actualiza el comentario de la venta
        UPDATE venta
        SET comentario = 'SIN ARTICULOS'
        WHERE idventa = idventa;
    END IF;
END$$
DELIMITER ;
