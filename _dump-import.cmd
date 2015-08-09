set db_name="bestoperator"
set username="bestoperator"
set pass="iemthebest"
set dumpfile="back.data"
mysql -u%username% -p%pass% --database %db_name%<%dumpfile%
pause