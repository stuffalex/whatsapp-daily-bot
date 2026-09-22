import sys
import time
from playwright.sync_api import sync_playwright
from config import SESSION_DIR

def run_setup() -> bool:
    print("=" * 60)
    print("Iniciando configuração da sessão do WhatsApp Web...")
    print(f"Diretório de dados da sessão: {SESSION_DIR}")
    print("=" * 60)

    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Tenta com Google Chrome do sistema, senão recorre ao Chromium padrão
        try:
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,
                channel="chrome",
                args=["--no-sandbox", "--disable-dev-shm-usage"],
                viewport={"width": 1280, "height": 800}
            )
        except Exception:
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
                viewport={"width": 1280, "height": 800}
            )

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        page.goto("https://web.whatsapp.com/")

        print("\n[AÇÃO NECESSÁRIA]")
        print("1. Abra o WhatsApp no seu celular.")
        print("2. Vá em Configurações/Ajustes > Aparelhos conectados > Conectar um aparelho.")
        print("3. Aponte a câmera para o QR Code na janela do navegador que se abriu.\n")
        print("Aguardando login (você tem até 3 minutos)...")

        success_selectors = [
            "#side",
            "#pane-side",
            'div[aria-label="Lista de conversas"]',
            'div[aria-label="Chat list"]',
            'header[data-testid="chatlist-header"]'
        ]

        logged_in = False
        start_time = time.time()
        timeout_seconds = 180

        while time.time() - start_time < timeout_seconds:
            for selector in success_selectors:
                try:
                    if page.locator(selector).is_visible():
                        logged_in = True
                        break
                except Exception:
                    pass

            if logged_in:
                break
            time.sleep(2)

        if logged_in:
            print("\n" + "=" * 60)
            print("SUCESSO: WhatsApp conectado e sessão salva com sucesso!")
            print(f"Os dados de autenticação foram gravados em: {SESSION_DIR}")
            print("=" * 60)
            print("Aguardando sincronização inicial (5 segundos)...")
            time.sleep(5)
        else:
            print("\n[AVISO]: O tempo limite para leitura do QR Code expirou.")
            print("Se você já escaneou, execute este script novamente para verificar.")

        browser_context.close()
        return logged_in

if __name__ == "__main__":
    try:
        success = run_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Erro ao executar setup: {e}", file=sys.stderr)
        sys.exit(1)
