@echo off
REM Cambia el directorio actual al directorio del script
cd /d %~dp0

REM Crear el entorno virtual en el directorio "venv"
python -m venv venv

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar dependencias desde requirements.txt
pip install -r requirements.txt

echo.
echo Instalación completada. El entorno virtual está activo.
echo Para activar el entorno virtual en futuras sesiones, ejecuta:
echo.
echo     call venv\Scripts\activate.bat
echo.
pause