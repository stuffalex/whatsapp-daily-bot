@echo off
title Remover Tarefa do Agendador do Windows
echo ========================================================
echo Removendo tarefa agendada do Windows...
echo ========================================================
powershell -ExecutionPolicy Bypass -File .\remove_task_windows.ps1
echo.
pause
