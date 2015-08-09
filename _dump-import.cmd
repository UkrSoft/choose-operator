@echo off
set db_name="bestoperator"
set username="bestoperator"
set pass="iamthebest"
set current_location=%~dp0
set dump_location=%current_location%dump\
set utils_location=%dump_location%utils\
set back_db_file=back.data
set full_dump_path=%dump_location%%back_db_file%
echo Are you READY for the show?
pause >nul

echo Extracting dump file...
"%utils_location%7z.exe" x "%full_dump_path%.zip" -o"%dump_location%" >nul
if errorlevel 1 (
goto :exit_label
) else (
echo OK.
)

echo Flusing the database...
mysql -b -u%username% -p%pass% < _mysql_recreate.sql
if errorlevel 1 (
goto :exit_label
) else (
echo OK.
)

echo Importing dump file into database...
mysql -u%username% -p%pass% --database %db_name%<"%full_dump_path%"
if errorlevel 1 (
goto :exit_label
) else (
echo OK.
)

echo Re-creating superuser (admin)
echo from django.contrib.auth.models import User; u,c = User.objects.get_or_create(username='admin'); u.set_password('111'); u.save(); | python manage.py shell >nul
if errorlevel 1 (
goto :exit_label
) else (
echo OK.
)

echo Deleting dump file...
del "%full_dump_path%"
if errorlevel 1 (
goto :exit_label
) else (
echo OK.
)
echo Finished! Be creative and push ANY key.
pause >nul
exit

:exit_label
echo Operation FAILED!
pause
exit 1