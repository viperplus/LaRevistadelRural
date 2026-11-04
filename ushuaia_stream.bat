@echo off
title Ushuaia Stream URL
for /f "delims=" %%i in ('python "%~dp0get_stream.py"') do set STREAM=%%i
echo.
echo ============================================
echo   URL del stream (copia y pega en OBS):
echo ============================================
echo.
echo   %STREAM%
echo.
echo ============================================
echo.
echo | set /p="%STREAM%"| clip
echo [OK] URL copiada al portapapeles. Pegala en OBS como "Entrada multimedia (VLC)".
echo.
pause
