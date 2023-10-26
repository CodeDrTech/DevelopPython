USE [Ventas]
GO

INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'HM', N'HERRAMIENTAS MANUALES')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'HE', N'HERRAMIENTAS EL�CTRICAS')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'FC', N'FERRETER�A PARA LA CONSTRUCCI�N')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'SF', N'SUMINISTROS PARA FONTANER�A')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'SE', N'SUMINISTROS EL�CTRICOS')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'PYC', N'PINTURA Y ACABADOS')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'SYP', N'SEGURIDAD Y PROTECCI�N')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'JYE', N'JARDINER�A Y EXTERIOR')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'AYO', N'ALMACENAMIENTO Y ORGANIZACI�N')
INSERT [dbo].[Categoria] ([nombre], [descripcion]) VALUES (N'DDI', N'DECORACI�N Y DISE�O DE INTERIORES')
GO


INSERT [dbo].[presentacion] ([nombre], [descripcion]) VALUES (N'UND', N'UNIDAD')
INSERT [dbo].[presentacion] ([nombre], [descripcion]) VALUES (N'GL', N'GALON')
INSERT [dbo].[presentacion] ([nombre], [descripcion]) VALUES (N'LT', N'LATA')
INSERT [dbo].[presentacion] ([nombre], [descripcion]) VALUES (N'PQT', N'PAQUETE')
INSERT [dbo].[presentacion] ([nombre], [descripcion]) VALUES (N'LB', N'LIBRA')
INSERT [dbo].[presentacion] ([nombre], [descripcion]) VALUES (N'KG', N'KILO GRAMO')
GO


INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00000', N'PINTURAS POPULAR', N'UN GALON DE PINTURA BLANCA', NULL, 6, 1)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00001', N'PINTURA POPULAR', N'COLOR AZUL (1 GL)', NULL, 6, 1)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00002', N'CLAVOS TITAN', N'CLAVOS DE ACERO DE UNA PULGADA', NULL, 3, 5)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00003', N'CLAVO TITAN', N'CLAVOS DE ACERO DE DOS PULGADAS', NULL, 3, 5)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00004', N'Martillo de carpintero', N'Martillo de carpintero de 16 oz con mango de madera resistente.', NULL, 2, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00005', N'Juego de destornilladores de precisi�n', N'Juego de 6 destornilladores de precisi�n con puntas intercambiables para trabajos delicados.', NULL, 2, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00006', N'Llave ajustable de 10"', N'Llave ajustable de 10" con mecanismo de trinquete para un ajuste r�pido y preciso.', NULL, 2, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00007', N'Sierra de mano plegable', N'Sierra de mano plegable con hoja dentada de acero para cortes limpios en madera y metal.', NULL, 2, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00008', N'Alicate de punta larga', N'Alicate de punta larga de 6" para trabajos de agarre y torsi�n en espacios estrechos.', NULL, 2, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00009', N'Taladro percutor de 18V', N'Taladro percutor inal�mbrico de 18V con velocidad variable y funci�n de percusi�n para perforaciones precisas.', NULL, 3, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00010', N'Sierra circular de 7-1/4"', N'Sierra circular de 7-1/4" con gu�a l�ser y ajuste de profundidad para cortes precisos en madera y otros materiales.', NULL, 3, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00011', N'Pulidora orbital de 6"', N'Pulidora orbital de 6" con velocidad variable y almohadillas de pulido para darle brillo a superficies.', NULL, 3, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00012', N'Lijadora orbital aleatoria', N'Lijadora orbital aleatoria de 5" con recolecci�n de polvo y sistema de fijaci�n de lijas.', NULL, 3, 3)
INSERT [dbo].[articulo] ([codigo], [nombre], [descripcion], [imagen], [idcategoria], [idpresentacion]) VALUES (N'ART00013', N'Pistola de calor de 1500W', N'Pistola de calor de 1500W con ajuste de temperatura y flujo de aire para trabajos de secado y encogimiento.', NULL, 3, 3)
GO

INSERT [dbo].[cliente] ([nombre], [apellidos], [sexo], [fecha_nacimiento], [tipo_documento], [num_documento], [direccion], [telefono], [email]) VALUES (N'CLIENTE', N'GENERICO', N'M', CAST(N'1900-01-01' AS Date), N'CEDULA', N'00000000000', N'CALLE #77', N'8091234567', NULL)
INSERT [dbo].[cliente] ([nombre], [apellidos], [sexo], [fecha_nacimiento], [tipo_documento], [num_documento], [direccion], [telefono], [email]) VALUES (N'JUAN JOSE', N'HERNANDEZ', N'M', CAST(N'1995-04-12' AS Date), N'CEDULA', N'09300765463', N'CALLE LA ESPERANZA #77', N'8096553425', NULL)
INSERT [dbo].[cliente] ([nombre], [apellidos], [sexo], [fecha_nacimiento], [tipo_documento], [num_documento], [direccion], [telefono], [email]) VALUES (N'MERCEDES', N'CAMILO', N'F', CAST(N'1990-01-10' AS Date), N'RNC', N'130762562', N'AVENIDA PRINCIPAL', N'8293647312', N'mercedes@hotmail.com')
GO


INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'JOSE', N'PEREZ', N'M', CAST(N'1990-10-20' AS Date), N'9300687598', N'CALLE PRIMERA LA CARTONERA', N'8298811831', N'joseperez8715@gmail.com', N'Administrador', N'admin', N'admin')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'JUAN', N'SANTOS', N'M', CAST(N'2000-02-09' AS Date), N'9837746652', N'CALLE PRIMERA LA CARTONERA', NULL, NULL, N'Vendedor', N'jose', N'1234')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'MARCELA', N'ADAMEZ', N'F', CAST(N'2000-02-09' AS Date), N'4028466536', NULL, NULL, NULL, N'Almacenista', N'luis', N'1234')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'JOSE LUIS', N'PEREZ', N'M', CAST(N'2000-01-05' AS Date), N'4038723787', NULL, NULL, NULL, N'Administrador', N'admin2', N'1234')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'DEMETRIO', N'CASILLA', N'M', CAST(N'2000-01-20' AS Date), N'3453453453', NULL, NULL, NULL, N'Vendedor', N'jose2', N'1234')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'MARCELINO', N'LOPEZ', N'M', CAST(N'1990-01-16' AS Date), N'3463678972', NULL, NULL, NULL, N'Almacenista', N'luis2', N'1234')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'PACHECO', N'CAMEJO', N'M', CAST(N'1987-10-27' AS Date), N'9300256587', NULL, NULL, NULL, N'Vendedor', N'camejo', N'2023')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'PEDRO', N'PALERMO', N'M', CAST(N'2000-01-01' AS Date), N'3489387494', NULL, NULL, NULL, N'Vendedor', N'palermo', N'1234')
INSERT [dbo].[empleado] ([nombre], [apellidos], [sexo], [fecha_nac], [num_documento], [direccion], [telefono], [email], [acceso], [usuario], [password]) VALUES (N'JUANCITO', N'CARVAJAR', N'M', CAST(N'2000-01-01' AS Date), N'2382763872', NULL, NULL, NULL, N'Vendedor', N'carvajar', N'2222')
GO


INSERT [dbo].[proveedor] ([razon_social], [sector_comercial], [tipo_documento], [num_documento], [direccion], [telefono], [email], [url]) VALUES (N'IMPORTADORA AMERICANA', N'TECNOLOGIA', N'RCN', N'132258964', N'CALLE PRINCIPAL # 13', N'8298811831', N'joseperez8715@gmail.com', NULL)
INSERT [dbo].[proveedor] ([razon_social], [sector_comercial], [tipo_documento], [num_documento], [direccion], [telefono], [email], [url]) VALUES (N'LAVANDERIA CARRASCO', N'SERVICIOS', N'RCN', N'131556987', N'CALLE LAS AMERICAS', N'8095326698', NULL, NULL)
GO
