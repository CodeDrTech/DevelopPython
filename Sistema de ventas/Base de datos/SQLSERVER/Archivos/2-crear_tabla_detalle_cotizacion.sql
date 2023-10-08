USE [Ventas]
GO

/****** Object:  Table [dbo].[detalle_venta]    Script Date: 10/7/2023 1:30:20 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[detalle_cotizacion](
	[iddetalle_cotizacion] [int] IDENTITY(1,1) NOT NULL,
	[idcotizacion] [int] NOT NULL,
	[iddetalle_ingreso] [int] NOT NULL,
	[cantidad] [int] NOT NULL,
	[precio_venta] [real] NOT NULL,
	[descuento] [real] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[iddetalle_cotizacion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[detalle_cotizacion]  WITH CHECK ADD FOREIGN KEY([iddetalle_ingreso])
REFERENCES [dbo].[detalle_ingreso] ([iddetalle_ingreso])
GO

ALTER TABLE [dbo].[detalle_cotizacion]  WITH CHECK ADD FOREIGN KEY([idcotizacion])
REFERENCES [dbo].[cotizacion] ([idcotizacion])
GO


