@echo off
set username="bestoperator"
set pass="iamthebest"

echo This will DROP existing DB and create it from the scratch!!!
echo.
echo ARE YOU SURE?
pause
mysql -b -u %username% -p%pass% < _mysql_recreate.sql
echo DONE.
pause