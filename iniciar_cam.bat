@echo off
title Tren del Fin del Mundo
echo ========================================
echo   Camara: Tren del Fin del Mundo
echo   URL: http://127.0.0.1:8765
echo ========================================
echo.
echo Iniciando server en segundo plano...
cscript //nologo "%~dp0start_server.vbs"
timeout /t 5 >nul
echo.
echo Server iniciado. Abrilo en OBS:
echo   Navegador -> http://127.0.0.1:8765
echo   1920x1080
echo.
echo Para ver si funciona, abri esta URL en Chrome:
echo   http://127.0.0.1:8765
echo.
pause
