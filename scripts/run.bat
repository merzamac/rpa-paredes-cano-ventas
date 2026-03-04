REM Hide the command prom pt window

@echo off
::auto-reiniciarse en segundo plano y minimizarse
if not "%1" == "h" ( 
    start /min cmd /C "%~dpnx0" h
    exit /b
)

title rpa_paredes_cano_ventas
cd ..
echo Changed to: %cd%

:loop

.\.venv\Scripts\python.exe -m src.rpa_paredes_cano_ventas

:: Esperar una hora antes de la próxima ejecución
timeout /t 60

:: Ir al comienzo del bucle
goto :loop