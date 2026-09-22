@echo off
title Status do Agendador em Segundo Plano
echo ========================================================
echo Verificando processos do Agendador em segundo plano...
echo ========================================================

tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /I "pythonw.exe" >nul

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [ATIVO] O Agendador esta RODANDO em segundo plano!
    tasklist /FI "IMAGENAME eq pythonw.exe"
) else (
    echo.
    echo [INATIVO] O Agendador em segundo plano NAO esta em execucao.
)
echo.
pause
