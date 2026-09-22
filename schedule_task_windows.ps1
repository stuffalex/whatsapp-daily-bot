# Script para criar a tarefa no Agendador de Tarefas do Windows (Task Scheduler)
# Executa em 100% segundo plano via pythonw.exe (sem janela preta de terminal)

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$EnvFile = Join-Path $CurrentDir ".env"
$MessagesJson = Join-Path $CurrentDir "mensagens.json"
$TaskName = "WhatsAppDailyBot"

# Prefere pythonw.exe para rodar sem abrir console/janela preta
$PythonPath = (Get-Command pythonw -ErrorAction SilentlyContinue).Source
if (-not $PythonPath) {
    $PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
}

if (-not $PythonPath) {
    Write-Error "Python não foi encontrado no PATH do sistema. Certifique-se de que o Python está instalado."
    exit 1
}

$ScriptPath = Join-Path $CurrentDir "sender.py"

# Lê o horário: primeiro tenta em mensagens.json, senão no .env
$ScheduleTime = "09:00"
if (Test-Path $MessagesJson) {
    try {
        $json = Get-Content $MessagesJson -Raw | ConvertFrom-Json
        if ($json.mensagem_1 -and $json.mensagem_1.horario) {
            $ScheduleTime = $json.mensagem_1.horario
        }
    } catch {}
} elseif (Test-Path $EnvFile) {
    $Lines = Get-Content $EnvFile
    foreach ($line in $Lines) {
        if ($line -match "^SCHEDULE_TIME=(.+)$") {
            $ScheduleTime = $Matches[1].Trim()
        }
    }
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Configurando Agendador do Windows (100% Invisivel)" -ForegroundColor Cyan
Write-Host " Horario diario: $ScheduleTime" -ForegroundColor Green
Write-Host " Script: $ScriptPath" -ForegroundColor Green
Write-Host " Executavel silencioso: $PythonPath" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# Registra usando schtasks
$Command = "schtasks /Create /F /TN `"$TaskName`" /TR `"`"$PythonPath`" `"$ScriptPath`"`" /SC DAILY /ST $ScheduleTime"

Invoke-Expression $Command

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCESSO] Tarefa agendada '$TaskName' criada com sucesso!" -ForegroundColor Green
    Write-Host "O Windows executara o script as $ScheduleTime DIARIAMENTE em SEGUNDO PLANO." -ForegroundColor Yellow
    Write-Host "Nenhuma janela de terminal ficara aberta." -ForegroundColor Yellow
} else {
    Write-Host "`n[AVISO] Se o comando falhou por permissao, execute o terminal como Administrador." -ForegroundColor Red
}
