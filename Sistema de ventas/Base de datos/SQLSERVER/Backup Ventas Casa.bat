sqlcmd -S localhost -d Ventas -U sa -P Jose.Luis.8715 -Q "BACKUP DATABASE Ventas TO DISK='C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Backup\Ventas.bak'" && copy /Y "C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Backup\Ventas.bak" "C:\Users\Jose\Documents\GitHub\DevelopPython\Sistema de ventas\Base de datos\SQLSERVER\"