sqlcmd -S localhost -d master -U sa -P Jose.Luis.8715 -Q "RESTORE DATABASE Ventas FROM DISK='C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\Backup\Ventas.bak' WITH REPLACE"
