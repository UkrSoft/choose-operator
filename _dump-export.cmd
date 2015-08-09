set db_name="quest"
set back_db_name=%db_name%_back_%date:~0,2%_%date:~6,4%_%date:~3,2%_%time:~0,2%_%time:~3,2%
set username="root"
set pass="111"

md ..\back\
mysqldump -u%username% -p%pass% --database %db_name% > ..\back\%back_db_name%.data
cd ..\back
zip %back_db_name%.zip *%back_db_name%*.data
del *%back_db_name%*.data