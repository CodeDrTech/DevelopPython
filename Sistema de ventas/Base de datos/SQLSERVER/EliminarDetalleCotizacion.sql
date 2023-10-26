USE [Ventas]
GO

/****** Object:  StoredProcedure [dbo].[EliminarDetalleCotizacion]    Script Date: 10/26/2023 1:45:40 PM *****/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[EliminarDetalleCotizacion]
    @id_detalle_cotizacion INT
AS
BEGIN
    -- Declarar variables locales
    DECLARE @idcotizacion INT;

    -- Obtener el idcotizacion desde el detalle
    SELECT @idcotizacion = idcotizacion
    FROM detalle_cotizacion
    WHERE iddetalle_cotizacion = @id_detalle_cotizacion;

    -- Eliminar el detalle de cotizacion
    DELETE FROM detalle_cotizacion
    WHERE iddetalle_cotizacion = @id_detalle_cotizacion;

    -- Comprobar si la cotización ya no tiene más detalles
    DECLARE @num_detalles INT;
    SELECT @num_detalles = COUNT(*)
    FROM detalle_cotizacion
    WHERE idcotizacion = @idcotizacion;

    IF @num_detalles <= 1
    BEGIN
        -- Eliminar la cotización y sus detalles
        DELETE FROM cotizacion
        WHERE idcotizacion = @idcotizacion;
    END;
END
GO


