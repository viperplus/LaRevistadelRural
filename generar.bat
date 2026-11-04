@echo off
title Generar cam.html para OBS
python "%~dp0generar_cam.py"
echo.
echo Listo. Abre OBS -> Fuentes -> + -> Navegador
echo URL: file:///%~dp0cam.html
echo Ancho: 1920  Alto: 1080
echo.
pause
