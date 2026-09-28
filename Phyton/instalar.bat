@echo off
setlocal enabledelayedexpansion
title SIGEPE - Instalador y verificador
color 0A

cd /d "%~dp0"

echo.
echo ==============================================================
echo   SIGEPE - Instalador y verificador
echo   Sistema de Gestion de Envios y Paqueteria Empresarial
echo ==============================================================
echo.

REM ---------------------------------------------------------------
REM  1. Buscar Python
REM ---------------------------------------------------------------
echo [1/6] Buscando Python...

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)

if not defined PY (
    echo.
    echo   [X] NO SE ENCONTRO PYTHON.
    echo.
    echo   Descargalo desde:  https://www.python.org/downloads/
    echo   IMPORTANTE: al instalar, marca la casilla
    echo   "Add Python to PATH" y luego elige "Customize installation"
    echo   y deja marcada la opcion "tcl/tk and IDLE".
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('%PY% -c "import sys;print(sys.version)" 2^>nul') do set "VER=%%v"
echo       Python detectado: !VER!

REM ---------------------------------------------------------------
REM  2. Version minima 3.9
REM ---------------------------------------------------------------
echo [2/6] Verificando la version de Python...

%PY% -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)"
if errorlevel 1 (
    echo.
    echo   [X] Se necesita Python 3.9 o superior.
    echo   Instala la version mas reciente desde https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo       Version correcta.

REM ---------------------------------------------------------------
REM  3. tkinter
REM ---------------------------------------------------------------
echo [3/6] Verificando la interfaz grafica (tkinter)...

%PY% -c "import tkinter" >nul 2>nul
if errorlevel 1 (
    echo.
    echo   [!] NO HAY TKINTER: la ventana grafica no estara disponible.
    echo       El sistema seguira funcionando con el menu de consola.
    echo       Para instalarlo en Windows, vuelve a ejecutar el instalador
    echo       de Python y marca "Modify" ^> "tcl/tk and IDLE".
    echo.
) else (
    echo       tkinter disponible: la ventana grafica funcionara.
)

REM ---------------------------------------------------------------
REM  4. Estructura de carpetas
REM ---------------------------------------------------------------
echo [4/6] Verificando la estructura de carpetas...

set "FALTAN="
for %%D in (modelos estructura_datos utilidades procesos interfaz pruebas) do (
    if not exist "%%D\" set "FALTAN=!FALTAN! %%D"
)

%PY% -c "import estructura_datos.colas, estructura_datos.pilas, estructura_datos.listas" >nul 2>nul
if errorlevel 1 (
    echo       [X] Faltan modulos o la estructura esta incompleta:!FALTAN!
    echo.
    pause
    exit /b 1
)
echo       Estructura completa.

REM ---------------------------------------------------------------
REM  5. Compilacion
REM ---------------------------------------------------------------
echo [5/6] Compilando el codigo...

%PY% -m compileall -q . >nul 2>nul
if errorlevel 1 (
    echo       [!] Hay errores de sintaxis. Revisa los mensajes de arriba.
) else (
    echo       Todo el codigo compila correctamente.
)

REM ---------------------------------------------------------------
REM  6. Pruebas automaticas
REM ---------------------------------------------------------------
echo [6/6] Ejecutando las pruebas automaticas...
echo.

%PY% main.py --pruebas
set "PRUEBAS=%errorlevel%"

echo.
if "%PRUEBAS%"=="0" (
    echo   [OK] Todas las pruebas pasaron.
) else (
    echo   [X] Hubo fallos en las pruebas. Revisa el detalle de arriba.
)

echo.
echo ==============================================================
echo   INSTALACION COMPLETADA
echo.
echo   Para abrir la ventana grafica:   main.py
echo   Para usar el menu de consola:    main.py --consola
echo   Para correr las pruebas:         main.py --pruebas
echo.
echo   Tambien puedes dar doble clic en  iniciar.bat
echo ==============================================================
echo.

choice /C SN /N /M "   Quieres abrir la aplicacion ahora? (S/N): "
if errorlevel 2 goto :fin
start "" pythonw main.py
goto :fin

:fin
echo.
pause
endlocal
