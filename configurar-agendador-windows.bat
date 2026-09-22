@echo off
title Configurar Agendador do Windows
echo ========================================================
echo Criando tarefa no Agendador do Windows (Task Scheduler)...
echo ========================================================
powershell -ExecutionPolicy Bypass -File .\schedule_task_windows.ps1
echo.
pause
