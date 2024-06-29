@echo off
cd "project root path"
set "app_id="
set "script_name=%~n0"
call venv\Scripts\activate
set "app_id=%app_id%"
start cmd /k "python -u main.py & timeout /t 5 & exit"