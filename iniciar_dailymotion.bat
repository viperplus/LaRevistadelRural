@echo off
title Dailymotion - Costanera de Posadas
echo ========================================
echo   Dailymotion: Costanera de Posadas
echo   Video: x9x6vqm
echo ========================================
echo.
echo Iniciando servidor en segundo plano...
cscript //nologo "%~dp0start_dailymotion.vbs"
timeout /t 6 >nul
echo.
echo En OBS: Fuentes - Agregar - Fuente de medios
echo y en "Archivo o URL" pegá:
echo.
echo   http://127.0.0.1:8771/proxy/m.m3u8
echo.
echo Para verla en Chrome, abrí:
echo   http://127.0.0.1:8771
echo.
echo Para apagar, cerrá el proceso python.
echo.
pause
