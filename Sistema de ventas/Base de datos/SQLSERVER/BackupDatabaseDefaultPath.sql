CREATE PROCEDURE dbo.BackupDatabaseDefaultPath
AS
BEGIN
    -- Genera la fecha actual en formato AAAAMMDDHHMMSS
    DECLARE @BackupFileDate NVARCHAR(20)
    SET @BackupFileDate = REPLACE(CONVERT(NVARCHAR(20), GETDATE(), 120), ':', '')

    -- Nombre del archivo de copia de seguridad con la fecha actual
    DECLARE @BackupFileName NVARCHAR(260)
    SET @BackupFileName = 'BackupDatabase_' + @BackupFileDate + '.bak'

    -- Ejecuta la copia de seguridad de la base de datos en la ruta por defecto
    BACKUP DATABASE Ventas TO DISK = @BackupFileName
END
