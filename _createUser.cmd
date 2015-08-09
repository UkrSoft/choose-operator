@echo off
set username="admin"
set email="admin@example.com"
:: pass supposed to be 111
python manage.py createsuperuser --username=%username% --email=%email%
pause