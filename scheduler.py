import time
import sys
import argparse
import schedule
from datetime import datetime

import config
from sender import send_whatsapp_message, log_event

def job(preset_key=None):
    tag = f" [{preset_key}]" if preset_key else ""
    log_event(f"Disparo agendado iniciado{tag}...")
    success = send_whatsapp_message(preset_key=preset_key)
    if success:
        log_event(f"Disparo agendado{tag} finalizado com êxito.")
    else:
        log_event(f"Disparo agendado{tag} finalizado com falhas. Verifique disparos.log.")

def main():
    parser = argparse.ArgumentParser(description="Agendador Diário do WhatsApp Bot")
    parser.add_argument("--now", action="store_true", help="Executa o disparo imediatamente sem esperar o horário agendado")
    parser.add_argument("--preset", default=None, help="Chave da mensagem a disparar (ex: mensagem_1)")
    args = parser.parse_args()

    if args.now:
        print("\n[MODO MANUAL] Executando disparo imediato...")
        job(preset_key=args.preset)
        return

    presets = config.load_presets()
    registered_count = 0

    print("=" * 65)
    print("           WHATSAPP DAILY BOT - AGENDADOR EM EXECUÇÃO")
    print("=" * 65)

    if presets:
        for key, item in presets.items():
            if item.get("ativo", True):
                horario = item.get("horario", "09:00")
                contato = item.get("contato", "Contato")
                telefone = item.get("telefone", "")
                
                # Registra o job no horário especificado
                schedule.every().day.at(horario).do(job, preset_key=key)
                registered_count += 1
                print(f"-> Agendado: [{key}] {contato} ({telefone}) às {horario} diariamente")
    
    if registered_count == 0:
        try:
            schedule_time = config.get_schedule_time()
            phone = config.get_phone_number()
            schedule.every().day.at(schedule_time).do(job)
            print(f"-> Agendado (via .env): Destino {phone} às {schedule_time} diariamente")
        except Exception as e:
            print(f"Erro de configuração: {e}")
            sys.exit(1)

    print("=" * 65)
    print("Agendador ativo. Pressione Ctrl + C para encerrar.")
    print("=" * 65)

    try:
        while True:
            schedule.run_pending()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nAgendador encerrado pelo usuário.")

if __name__ == "__main__":
    main()
