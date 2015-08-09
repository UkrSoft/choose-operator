@echo off
set db_name="bestoperator"
set username="bestoperator"
set pass="iamthebest"
set current_location=%~dp0
set dump_location=%current_location%dump\
set utils_location=%dump_location%utils\
set back_db_file=back.data
set full_dump_path=%dump_location%%back_db_file%
echo Creating dump file...
mysqldump -u%username% -p%pass% --database %db_name% > "%full_dump_path%"
if errorlevel 1 (
goto :exit_label
) else (
echo OK.
)
echo Zipping dump file...
"%utils_location%7z.exe" a "%full_dump_path%.zip" "%full_dump_path%" -o{"%dump_location%"} >nul
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
pause
exit
:exit_label
echo Operation FAILED!
pause
exit 1