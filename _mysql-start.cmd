@echo off
set db_name="bestoperator"
set username="bestoperator"
set pass="iamthebest"

mysql -b -u %username% -p%pass% %db_name%
pause