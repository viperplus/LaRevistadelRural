@echo off
title Auto-refresh cada 2 horas
:loop
python "%~dp0generar_cam.py" >> "%~dp0refresh.log" 2>&1
timeout /t 7200 /nobreak >nul
goto loop
