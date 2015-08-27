@echo off
cd ..
python manage.py makemessages -l uk
python manage.py makemessages -l ru
pause