import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

import config

LOG_FILE = config.BASE_DIR / "disparos.log"

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"Erro ao salvar no arquivo de log: {e}")

def send_whatsapp_message(phone: str = None, message: str = None, headless: bool = None, preset_key: str = None) -> bool:
    try:
        phone = phone or config.get_phone_number(preset_key)
        message = message or config.get_message(preset_key)
        if headless is None:
            headless = config.is_headless()
    except Exception as e:
        log_event(f"ERRO DE CONFIGURAÇÃO: {e}")
        return False

    if not config.SESSION_DIR.exists() or not any(config.SESSION_DIR.iterdir()):
        log_event(
            "ERRO: Nenhuma sessão salva encontrada em .session_data. "
            "Por favor, execute primeiro: python setup_session.py para conectar seu WhatsApp."
        )
        return False

    log_event(f"Iniciando envio para {phone}...")
    encoded_text = urllib.parse.quote(message)
    target_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_text}"

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    with sync_playwright() as p:
        try:
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=str(config.SESSION_DIR),
                headless=headless,
                channel="chrome",
                user_agent=user_agent,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ],
                viewport={"width": 1280, "height": 800}
            )
        except Exception:
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=str(config.SESSION_DIR),
                headless=headless,
                user_agent=user_agent,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ],
                viewport={"width": 1280, "height": 800}
            )

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

        try:
            log_event("Carregando WhatsApp Web...")
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)

            # Aguarda a tela de carregamento inicial do WhatsApp terminar
            # Verifica se apareceu tela de QR code (o que indicaria sessão expirada/desconectada)
            qr_selector = 'canvas[aria-label="Scan this QR code to use WhatsApp Web"], canvas[aria-label="Scan me!"]'
            
            # Seletores para caixa de mensagem e botão de envio exclusivo
            input_box_selector = 'footer div[contenteditable="true"], div[data-tab="10"], div[data-lexical-editor="true"], footer p.selectable-text'
            send_btn_selector = (
                'button[aria-label="Enviar"], '
                'button[aria-label="Send"], '
                'button:has(span[data-icon="send"]), '
                'span[data-icon="send"], '
                '[data-testid="send"], '
                '[data-icon="send"]'
            )
            invalid_phone_selector = 'div[data-animate-modal-popup="true"]'

            success = False
            start_wait = time.time()
            max_wait = 70

            captured_debug = False

            while time.time() - start_wait < max_wait:
                # 1. Checa se a sessão caiu
                try:
                    if page.locator(qr_selector).is_visible():
                        log_event("ERRO: WhatsApp desconectado. A sessão expirou. Execute 'python setup_session.py' novamente.")
                        browser_context.close()
                        return False
                except Exception:
                    pass

                # 2. Checa se o número de telefone é inválido
                try:
                    if page.locator(invalid_phone_selector).is_visible():
                        popup_text = page.locator(invalid_phone_selector).inner_text()
                        if "url" in popup_text.lower() or "número" in popup_text.lower() or "invalid" in popup_text.lower():
                            log_event(f"ERRO: Número de telefone inválido no WhatsApp ({phone}). Detalhes: {popup_text}")
                            browser_context.close()
                            return False
                except Exception:
                    pass

                # Se já passou 15s e ainda não enviou, tira um screenshot para diagnóstico
                if not captured_debug and time.time() - start_wait > 15:
                    captured_debug = True
                    try:
                        debug_path = config.BASE_DIR / "debug_screen.png"
                        page.screenshot(path=str(debug_path))
                        log_event(f"Screenshot de depuração salvo em {debug_path.name}")
                        # Verifica se #main ou #side estão visíveis
                        side_vis = page.locator("#side").is_visible()
                        main_vis = page.locator("#main").is_visible()
                        log_event(f"Status da página - Menu lateral (#side): {side_vis} | Painel de conversa (#main): {main_vis}")
                    except Exception as err:
                        log_event(f"Aviso de depuração: {err}")

                # 3. Localiza a caixa de mensagem
                # Procura por qualquer div contenteditable dentro do #main ou footer
                try:
                    # Tenta seletor amplo de caixa de texto
                    input_boxes = page.locator('#main footer div[contenteditable="true"], footer div[contenteditable="true"], div[data-tab="10"], div[data-lexical-editor="true"]')
                    if input_boxes.count() > 0 and input_boxes.first.is_visible():
                        input_box = input_boxes.first
                        time.sleep(1)
                        current_text = input_box.inner_text().strip()
                        if not current_text:
                            input_box.click()
                            page.keyboard.type(message)
                            time.sleep(0.5)

                        input_box.click()
                        time.sleep(0.5)
                        page.keyboard.press("Enter")
                        log_event("Mensagem enviada via Enter na caixa de texto!")
                        success = True
                        break
                except Exception:
                    pass

                # 4. Alternativa: clica estritamente no botão de envio
                try:
                    send_btn = page.locator(send_btn_selector).first
                    if send_btn.is_visible() and send_btn.is_enabled():
                        time.sleep(0.5)
                        send_btn.click()
                        log_event("Botão de envio clicado com sucesso!")
                        success = True
                        break
                except Exception:
                    pass

                # 5. Verifica se há algum botão como 'Continuar para a conversa' ou 'Iniciar conversa'
                try:
                    start_chat_btn = page.locator('text="Continuar para a conversa", text="Iniciar conversa", text="Abrir no WhatsApp Web", a[href*="whatsapp.com"]').first
                    if start_chat_btn.is_visible():
                        start_chat_btn.click()
                        time.sleep(2)
                except Exception:
                    pass

                time.sleep(2)

            if success:
                # Aguarda alguns segundos para garantir que os pacotes de rede do envio foram transmitidos
                time.sleep(5)
                log_event(f"SUCESSO: Mensagem enviada para {phone}!")
            else:
                log_event("FALHA: Tempo esgotado aguardando o carregamento da conversa ou botão de envio.")

            browser_context.close()
            return success

        except Exception as e:
            log_event(f"ERRO durante o processo de envio: {e}")
            try:
                browser_context.close()
            except Exception:
                pass
            return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Envio de mensagem via WhatsApp")
    parser.add_argument("--phone", help="Número de destino (DDI + DDD + Telefone)")
    parser.add_argument("--message", help="Mensagem de texto a enviar")
    parser.add_argument("--headless", action="store_true", help="Rodar com navegador oculto")
    parser.add_argument("--visible", action="store_true", help="Forçar navegador visível")

    args = parser.parse_args()

    hl = None
    if args.headless:
        hl = True
    elif args.visible:
        hl = False

    # Se um telefone específico foi passado na linha de comando, dispara apenas para ele
    if args.phone:
        result = send_whatsapp_message(phone=args.phone, message=args.message, headless=hl)
        sys.exit(0 if result else 1)

    # Caso contrário (chamada do Agendador diário), processa todos os contatos ativos do mensagens.json
    presets = config.load_presets()
    if presets:
        overall_success = True
        active_presets = [k for k, v in presets.items() if v.get("ativo", True)]
        log_event(f"Iniciando rotina diária para {len(active_presets)} contato(s) ativo(s)...")

        for key in active_presets:
            item = presets[key]
            contato = item.get("contato", key)
            log_event(f"--- Processando [{key}] {contato} ---")
            success = send_whatsapp_message(preset_key=key, headless=hl)
            if not success:
                overall_success = False
            # Pausa de 5 segundos entre mensagens para segurança
            time.sleep(5)

        log_event("Rotina diária concluída.")
        sys.exit(0 if overall_success else 1)
    else:
        # Fallback para o .env padrão
        result = send_whatsapp_message(headless=hl)
        sys.exit(0 if result else 1)
