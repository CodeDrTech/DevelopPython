USE [Ventas]
GO

/****** Object:  Table [dbo].[cotizacion]]   Script Date: 10/7/2023 1:21:25 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[cotizacion](
	[idcotizacion] [int] IDENTITY(1,1) NOT NULL,
	[idcliente] [int] NOT NULL,
	[idempleado] [int] NOT NULL,
	[fecha] [date] NOT NULL,
	[tipo_comprobante] [int] NOT NULL,
	[serie] [nvarchar](max) NOT NULL,
	[itbis] [real] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idcotizacion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[cotizacion]  WITH CHECK ADD FOREIGN KEY([idcliente])
REFERENCES [dbo].[cliente] ([idcliente])
GO

ALTER TABLE [dbo].[cotizacion]  WITH CHECK ADD FOREIGN KEY([idempleado])
REFERENCES [dbo].[empleado] ([idempleado])
GO

