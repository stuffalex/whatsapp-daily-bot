@echo off
title Parar Agendador em Segundo Plano
echo ========================================================
echo Encerrando processos do Agendador em segundo plano...
echo ========================================================

taskkill /F /IM pythonw.exe 2>nul

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCESSO] O agendador em segundo plano foi encerrado com sucesso.
) else (
    echo.
    echo [INFO] Nenhum agendador em segundo plano estava em execucao.
)
echo.
pause
