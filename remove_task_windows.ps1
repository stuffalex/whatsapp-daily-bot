# Script para remover a tarefa do Agendador de Tarefas do Windows

$TaskName = "WhatsAppDailyBot"

Write-Host "Removendo tarefa agendada: $TaskName..." -ForegroundColor Cyan
schtasks /Delete /TN "$TaskName" /F

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCESSO] Tarefa '$TaskName' removida com sucesso do Agendador de Tarefas." -ForegroundColor Green
} else {
    Write-Host "[AVISO] Nao foi possivel remover a tarefa. Verifique se ela existia ou se requer permissao de Administrador." -ForegroundColor Yellow
}
