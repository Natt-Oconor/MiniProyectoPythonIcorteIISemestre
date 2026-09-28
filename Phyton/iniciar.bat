@echo off
title SIGEPE - Sistema de Gestion de Envios
cd /d "%~dp0"

REM Abre la aplicacion en la ventana grafica.
REM Si no encuentra tkinter, main.py cae solo al menu de consola.

python main.py %*
if errorlevel 1 (
    echo.
    echo No se pudo iniciar con 'python'. Probando con el lanzador 'py'...
    py -3 main.py %*
)
