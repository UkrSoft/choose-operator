@echo off
echo This will DROP existing DB and create it from the scratch!!!
echo.
echo ARE YOU SURE?
pause
mysql -b -u root -p1111 bestoperator < recreate.sql
echo DONE!
pause