@echo off
set DJANGO_SETTINGS_MODULE=qercas_project.settings
set PYTHONPATH=%~dp0

rem Use eventlet for better Windows compatibility
celery -A qercas_project worker --pool=solo -l info
