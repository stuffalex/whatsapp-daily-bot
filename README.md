# 📱 WhatsApp Daily Bot - Guia Completo e Documentação

Sistema automatizado em Python com Playwright para envio diário e programado de mensagens personalizadas no WhatsApp.
---
Para aqueles que desejarem contribuir para futuras manutenções:
Chave pix: 906d5175-89cb-4b07-8cee-385e47fbf549
---

## 📑 Sumário

1. [Visão Geral e Como Funciona](#-visão-geral-e-como-funciona)
2. [Onde Modificar as Configurações e o Scheduler](#-onde-modificar-as-configurações-e-o-scheduler)
3. [Como Rodar o Projeto (Passo a Passo)](#-como-rodar-o-projeto-passo-a-passo)
4. [Como Fazer o Scheduler Funcionar Diariamente](#-como-fazer-o-scheduler-funcionar-diariamente)
5. [Como Testar com Outro Número](#-como-testar-com-outro-número)
6. [Estrutura dos Arquivos](#-estrutura-dos-arquivos)
7. [Logs e Histórico de Envios](#-logs-e-histórico-de-envios)
8. [Perguntas Frequentes e Resolução de Problemas](#-perguntas-frequentes-e-resolução-de-problemas)

---

## 💡 Visão Geral e Como Funciona

- O bot utiliza um navegador Chromium controlado via **Playwright**.
- **Login único:** Você escaneia o QR Code do WhatsApp Web uma única vez. A sessão (cookies, tokens e cache) é salva localmente na pasta `.session_data/`.
- **Disparo:** No horário programado, o bot abre a conversa diretamente via URL com a mensagem pré-carregada, confirma o envio e registra o resultado no arquivo de log.
- **Gratuito e Seguro:** Não utiliza APIs pagas de terceiros nem expõe suas credenciais para fora do seu computador.

---

## 🛠 Onde Modificar as Configurações e o Scheduler

Você tem dois locais simples para configurar números, mensagens e horários:

### 1. No arquivo `mensagens.json` (Recomendado para presets e múltiplas mensagens)
Abra o arquivo [`mensagens.json`](mensagens.json) em qualquer editor de texto (Bloco de Notas, VS Code, etc.):

```json
{
  "mensagem_1": {
    "descricao": "Cobranca Debitos em Atraso",
    "contato": "Tatielly",
    "telefone": "5567999940776",
    "mensagem": "Bom dia, Tatielly! Consegue realizar o pagamento dos débitos em atraso no dia de hoje?\nValor total: R$ 6.200,00",
    "horario": "09:00",
    "ativo": true
  }
}
```

#### O que você pode alterar aqui:
- **`horario`**: O horário em que o scheduler irá disparar esta mensagem (formato 24h `HH:MM`, ex: `"08:30"`, `"14:00"`, `"19:45"`).
- **`telefone`**: O número de destino com DDI (55) + DDD (2 dígitos) + Número. Apenas números, sem traços ou parênteses.
- **`mensagem`**: O texto da mensagem. Use `\n` sempre que quiser quebrar para uma nova linha.
- **`contato`**: O nome da pessoa (usado para identificar no log e na mensagem).
- **`ativo`**: Mude para `false` caso queira pausar o envio desta mensagem sem apagá-la.

> [!TIP]
> Você pode cadastrar mais mensagens duplicando o bloco, por exemplo criando `"mensagem_2"`, `"mensagem_3"`, cada uma com seu próprio número, horário e mensagem!

---

### 2. No arquivo `.env` (Configuração Padrão / Variáveis de Ambiente)
Abra o arquivo [`.env`](.env):

```ini
CONTACT_NAME=Tatielly
PHONE_NUMBER=5567999940776
MESSAGE="Bom dia, Tatielly! Consegue realizar o pagamento dos débitos em atraso no dia de hoje?\nValor total: R$ 6.200,00"
SCHEDULE_TIME=09:00
HEADLESS=False
```

#### O que você pode alterar aqui:
- **`SCHEDULE_TIME`**: Horário padrão diário do agendamento (ex: `09:00`).
- **`PHONE_NUMBER`**: Número padrão de envio.
- **`MESSAGE`**: Mensagem padrão.
- **`HEADLESS`**: 
  - `False`: Você verá o navegador abrir na sua tela e enviar a mensagem.
  - `True`: O navegador enviará a mensagem de forma invisível em segundo plano (recomendado após validar que tudo está funcionando).

---

## 🚀 Como Rodar o Projeto (Passo a Passo)

Você pode operar tudo dando **dois cliques** nos arquivos `.bat` na pasta do projeto:

### Passo 1: Conectar o WhatsApp (Fazer uma única vez)
1. Dê dois cliques em **`1-conectar-whatsapp.bat`** (ou execute `python setup_session.py`).
2. Uma janela do navegador abrirá no WhatsApp Web.
3. No seu celular, abra o WhatsApp, vá em:
   **Configurações / Ajustes > Aparelhos Conectados > Conectar um aparelho**.
4. Aponte a câmera para o QR Code.
5. Assim que suas conversas carregarem, o terminal informará sucesso e a sessão estará salva na pasta `.session_data`.

---

### Passo 2: Fazer um Envio de Teste
- Para testar o envio para o número cadastrado (**Tatielly**):
  - Dê dois cliques em **`2-testar-envio.bat`** (ou execute `python sender.py`).
- Para testar com qualquer outro número de telefone:
  - Dê dois cliques em **`teste-com-outro-numero.bat`** (ou execute `python teste_rapido.py`).

---

## ⏰ Como Fazer o Scheduler Funcionar Diariamente

Existem **duas maneiras** de deixar o scheduler ativo:

### Método A: Agendador de Tarefas do Windows (Recomendado)
*O Windows se encarrega de disparar a automação no horário exato todos os dias, **sem precisar manter nenhuma janela de terminal aberta**.*

1. **Para ativar**:
   - Dê dois cliques no arquivo **`configurar-agendador-windows.bat`**.
   - O script lerá o horário definido no `mensagens.json` ou `.env` e registrará a tarefa `WhatsAppDailyBot` no Windows.
2. **Como conferir a tarefa no Windows**:
   - Pressione as teclas `Win + R`, digite `taskschd.msc` e tecle Enter.
   - Na lista "Biblioteca do Agendador de Tarefas", você verá `WhatsAppDailyBot` com o horário agendado e o próximo disparo.
3. **Para desativar / remover**:
   - Dê dois cliques em **`remover-agendador-windows.bat`**.

---

### Método B: Agendador Contínuo via Terminal
*Ideal se você já costuma deixar o computador ligado com janelas abertas ou em servidores.*

1. Dê dois cliques em **`3-iniciar-agendador-diario.bat`** (ou execute `python scheduler.py`).
2. O terminal mostrará todas as mensagens agendadas e ficará ativo aguardando o horário:
   ```
   =================================================================
              WHATSAPP DAILY BOT - AGENDADOR EM EXECUÇÃO
   =================================================================
   -> Agendado: [mensagem_1] Tatielly (5567999940776) às 09:00 diariamente
   =================================================================
   ```
3. Para encerrar, basta fechar a janela ou pressionar `Ctrl + C`.

---

## 🧪 Como Testar com Outro Número

Para enviar uma mensagem para um número diferente sem esperar horário:

1. Dê dois cliques em **`teste-com-outro-numero.bat`**.
2. Digite o número com DDD (exemplo: `67999998888` ou `5567999998888`).
3. Digite o texto desejado ou dê `Enter` para usar a mensagem de teste padrão.
4. O navegador abrirá e enviará a mensagem imediatamente.

Também pode ser executado via terminal:
```powershell
python teste_rapido.py --phone 5567999998888 --message "Ola, este e um teste!"
```

---

## 📁 Estrutura dos Arquivos

```
whatsapp-daily-bot/
├── mensagens.json                  # Catálogo de mensagens, contatos e horários agendados
├── .env                           # Configurações de ambiente (número, horário, headless)
├── config.py                      # Módulo de leitura e validação das configurações
├── sender.py                      # Motor de envio via Playwright no WhatsApp Web
├── scheduler.py                   # Agendador contínuo em Python
├── setup_session.py               # Script para autenticar e salvar o login do WhatsApp
├── teste_rapido.py                # Script de teste imediato com qualquer número
│
├── 1-conectar-whatsapp.bat        # [Atalho] Conectar WhatsApp pela 1ª vez
├── 2-testar-envio.bat             # [Atalho] Enviar mensagem de teste para mensagem_1
├── 3-iniciar-agendador-diario.bat # [Atalho] Iniciar o scheduler em janela de comando
├── teste-com-outro-numero.bat     # [Atalho] Testar envio imediato com outro número
├── configurar-agendador-windows.bat # [Atalho] Cadastrar tarefa no Agendador do Windows
├── remover-agendador-windows.bat  # [Atalho] Remover tarefa do Agendador do Windows
│
├── schedule_task_windows.ps1      # Script PowerShell de agendamento no Windows
├── remove_task_windows.ps1        # Script PowerShell de remoção do agendamento
├── disparos.log                   # Histórico de auditoria com data, hora e status de envio
├── requirements.txt               # Dependências do projeto (playwright, python-dotenv, schedule)
└── README.md                      # Este manual completo
```

---

## 📊 Logs e Histórico de Envios

Todas as tentativas de envio (tanto agendadas quanto testes manuais) são registradas no arquivo [`disparos.log`](disparos.log):

Exemplo de log registrado:
```
[2026-09-22 09:00:02] Iniciando envio para 5567999940776...
[2026-09-22 09:00:10] Carregando WhatsApp Web...
[2026-09-22 09:00:24] Botão de envio clicado!
[2026-09-22 09:00:29] SUCESSO: Mensagem enviada para 5567999940776!
```

Se ocorrer qualquer falha (número inválido, falta de internet, sessão expirada), o motivo exato será gravado no log.

---

## ❓ Perguntas Frequentes e Resolução de Problemas

#### 1. "O computador precisa estar ligado no horário programado?"
**Sim.** Como se trata de uma automação local (feita pelo seu computador sem custos com servidores de nuvem), o computador deve estar ligado ou com o Windows ativo no horário estipulado. Se o computador estiver desligado, o envio ocorrerá na próxima vez que a tarefa for executada.

#### 2. "Como alterar o horário do envio diário?"
1. Abra [`mensagens.json`](mensagens.json) (ou [`.env`](.env)) e altere o campo `"horario": "09:00"` para o novo horário desejado (ex: `"10:30"`).
2. Se estiver usando o Agendador do Windows, dê dois cliques em **`configurar-agendador-windows.bat`** para atualizar o horário no sistema.

#### 3. "Como enviar sem que a janela do navegador apareça?"
No arquivo [`.env`](.env), altere a linha:
```ini
HEADLESS=True
```
Assim que estiver como `True`, os disparos acontecerão silenciosamente em segundo plano.

#### 4. "O que fazer se aparecer a mensagem 'WhatsApp desconectado'?"
Isso acontece se você desconectar o aparelho pelo aplicativo do celular ou se a Meta revogar a sessão. Basta dar dois cliques em **`1-conectar-whatsapp.bat`** e escanear o QR Code novamente para restaurar a conexão.
