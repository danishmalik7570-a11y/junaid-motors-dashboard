@echo off
echo Starting Showroom Dashboard...
cd /d "%~dp0Django-Stack\cardealer"
python manage.py runserver 8000
pause
