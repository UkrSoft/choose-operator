@echo off
set username="bestoperator"
set pass="iamthebest"

echo This will DROP existing DB and create it from the scratch!!!
echo.
echo ARE YOU SURE?
pause
mysql -b -u %username% -p%pass% -e "drop database bestoperator;" >nul
mysql -b -u %username% -p%pass% -e "create database bestoperator;" >nul
echo DONE.
pause