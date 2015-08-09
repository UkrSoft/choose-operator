set db_name="bestoperator"
set username="bestoperator"
set pass="iamthebest"
set current_location=%~dp0
set dump_location=%current_location%dump\
set utils_location=%dump_location%utils\
set current_time=date.exe +"%Y-%m-%d %H-%M-%S"
set back_db_file=%db_name%_%current_time%

mysqldump -u%username% -p%pass% --database %db_name% > "%dump_location%%back_db_file%.data"
"%utils_location%"7z %dump_location%%back_db_file%.zip %dump_location%*%back_db_file%*.data -o{%dump_location%}
del %dump_location%*%back_db_file%*.data
pause