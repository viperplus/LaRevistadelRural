@echo off
title Auto-refresh camaras (cada 2h)
echo ========================================
echo   Refrescando URLs de camaras...
echo ========================================
python "%~dp0camaras.py"
echo.
echo ========================================
echo   Listo. Las playlists estan en:
echo   %~dp0playlists\
echo.
echo   Ahora ejecuta "refrescar.bat" en el
echo   inicio de Windows para que se actualice
echo   automaticamente cada vez que enciendas
echo   la PC.
echo ========================================
pause
