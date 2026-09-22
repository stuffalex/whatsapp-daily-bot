@echo off
title Iniciar Agendador em Segundo Plano
echo ========================================================
echo Iniciando o Agendador do WhatsApp em SEGUNDO PLANO...
echo ========================================================

:: Inicia o scheduler usando pythonw (sem janela preta de terminal)
start "" pythonw.exe scheduler.py

echo.
echo [SUCESSO] O Agendador ja esta rodando nos processos em segundo plano!
echo Nenhuma janela ficara aberta. O envio ocorrera no horario programado.
echo.
echo Para verificar se esta rodando: use 'status-segundo-plano.bat'
echo Para encerrar: use 'parar-segundo-plano.bat'
echo ========================================================
echo Esta janela fechara automaticamente em 4 segundos...
timeout /t 4 >nul
exit
