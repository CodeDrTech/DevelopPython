DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `RevertirVenta`(IN idventa INT)
BEGIN
    -- Declarar variables y cursores al inicio
    DECLARE idarticulo INT;
    DECLARE cantidad INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cursor_detalle CURSOR FOR 
        SELECT idarticulo, cantidad FROM detalle_venta WHERE idventa = idventa;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Cambiar el comentario de la venta a "DEVOLUCION DE VENTA"
    UPDATE venta
    SET comentario = 'DEVOLUCION DE VENTA'
    WHERE idventa = idventa;

    OPEN cursor_detalle;

    read_loop: LOOP
        FETCH cursor_detalle INTO idarticulo, cantidad;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Para cada articulo vendido, incrementar la cantidad disponible en la tabla de stock
        UPDATE stock
        SET disponible = disponible + cantidad
        WHERE idarticulo = idarticulo;
    END LOOP;

    CLOSE cursor_detalle;
END$$
DELIMITER ;
