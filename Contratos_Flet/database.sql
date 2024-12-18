-- Crear la base de datos
CREATE DATABASE Contratos;
GO

-- Usar la base de datos
USE Contratos;
GO

-- Tabla Usuario
CREATE TABLE Usuario (
    idUsuario INT IDENTITY(1,1) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cedula VARCHAR(13) NULL,
    numeroEmpleado VARCHAR(20) NULL,
    PRIMARY KEY (idUsuario)
);

-- Tabla Equipo
CREATE TABLE Equipo (
    idEquipo INT IDENTITY(1,1) NOT NULL,
    idUsuario INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    condicion VARCHAR(10) NULL CHECK (condicion IN ('Nuevo', 'Usado')),
    imei VARCHAR(100) NULL,
    PRIMARY KEY (idEquipo),
    FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario)
);

-- Tabla EquipoImagen
CREATE TABLE EquipoImagen (
    idImagen INT IDENTITY(1,1) NOT NULL,
    idEquipo INT NOT NULL,
    rutaImagen NVARCHAR(255) NOT NULL DEFAULT 'ruta_por_defecto',
    PRIMARY KEY (idImagen),
    FOREIGN KEY (idEquipo) REFERENCES Equipo (idEquipo)
);

-- Tabla Contrato
CREATE TABLE Contrato (
    idContrato INT IDENTITY(1,1) NOT NULL,
    numeroContrato VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    idUsuario INT NOT NULL,
    idEquipo INT NOT NULL,
    PRIMARY KEY (idContrato),
    FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario),
    FOREIGN KEY (idEquipo) REFERENCES Equipo (idEquipo)
);

-- Tabla Login
CREATE TABLE Login (
    idLogin INT IDENTITY(1,1) NOT NULL,
    usuario NVARCHAR(50) NOT NULL,
    contrasena NVARCHAR(255) NOT NULL,
    PRIMARY KEY (idLogin),
    UNIQUE (usuario)
);
