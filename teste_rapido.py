import sys
import re
import argparse
from config import SESSION_DIR
from sender import send_whatsapp_message
from setup_session import run_setup

def main():
    parser = argparse.ArgumentParser(description="Envio de teste rápido via WhatsApp")
    parser.add_argument("--phone", help="Número com DDD para envio de teste")
    parser.add_argument("--message", help="Mensagem para o teste")
    args = parser.parse_args()

    if not SESSION_DIR.exists() or not any(SESSION_DIR.iterdir()):
        print("=" * 60)
        print("Sessão do WhatsApp não encontrada. Vamos conectar pela primeira vez.")
        print("Uma janela será aberta para você escanear o QR Code no seu celular...")
        print("=" * 60)
        login_ok = run_setup()
        if not login_ok or not SESSION_DIR.exists() or not any(SESSION_DIR.iterdir()):
            print("\nO login não foi concluído. Execute novamente quando estiver pronto.")
            return

    # 2. Pede os dados se não foram passados por argumento
    phone = args.phone
    if not phone:
        print("\n" + "=" * 60)
        print("TESTE DE DISPARO RÁPIDO DO WHATSAPP")
        print("=" * 60)
        user_input = input("Digite o número de telefone de teste com DDD (ex: 67999999999 ou 5567999999999): ").strip()
        phone = re.sub(r"\D", "", user_input)
        if not phone:
            print("Número inválido ou não informado. Teste cancelado.")
            return
        # Se digitou sem DDI (55), adiciona automaticamente
        if len(phone) in (10, 11) and not phone.startswith("55"):
            phone = "55" + phone

    message = args.message
    if not message:
        default_msg = "Mensagem de teste automático do WhatsApp Bot. Envio realizado com sucesso!"
        msg_input = input(f"\nDigite a mensagem (ou tecle Enter para usar a mensagem padrão de teste):\n> ").strip()
        message = msg_input if msg_input else default_msg

    print(f"\n[ENVIANDO] Disparando para {phone}...")
    print(f"Mensagem: {message}")
    
    # Executa com navegador visível para você poder acompanhar
    success = send_whatsapp_message(phone=phone, message=message, headless=False)

    if success:
        print("\n" + "=" * 60)
        print(f"SUCESSO! Mensagem de teste enviada com sucesso para {phone}.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FALHA: Não foi possível enviar a mensagem. Verifique disparos.log para detalhes.")
        print("=" * 60)

if __name__ == "__main__":
    main()
