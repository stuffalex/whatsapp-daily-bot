import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
MESSAGES_JSON_PATH = BASE_DIR / "mensagens.json"
SESSION_DIR = BASE_DIR / ".session_data"

load_dotenv(dotenv_path=ENV_PATH)

def load_presets() -> dict:
    if MESSAGES_JSON_PATH.exists():
        try:
            with open(MESSAGES_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_presets(data: dict):
    with open(MESSAGES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_preset(preset_key: str = "mensagem_1") -> dict:
    presets = load_presets()
    if preset_key in presets:
        return presets[preset_key]
    return {}

def get_phone_number(preset_key: str = None) -> str:
    if preset_key:
        preset = get_preset(preset_key)
        if preset and "telefone" in preset:
            return re.sub(r"\D", "", preset["telefone"])
            
    raw_number = os.getenv("PHONE_NUMBER", "").strip()
    clean_number = re.sub(r"\D", "", raw_number)
    if not clean_number:
        # Tenta pegar da mensagem_1 como fallback
        preset1 = get_preset("mensagem_1")
        if preset1 and "telefone" in preset1:
            return re.sub(r"\D", "", preset1["telefone"])
        raise ValueError("O PHONE_NUMBER não foi definido nem no .env nem em mensagens.json.")
    if len(clean_number) < 10:
        raise ValueError(
            f"O número informado '{clean_number}' parece inválido. Certifique-se de incluir DDI e DDD (ex: 5567991240596)."
        )
    return clean_number

def get_contact_name(preset_key: str = None) -> str:
    if preset_key:
        preset = get_preset(preset_key)
        if preset and "contato" in preset:
            return preset["contato"]
    return os.getenv("CONTACT_NAME", "").strip()

def get_message(preset_key: str = None) -> str:
    if preset_key:
        preset = get_preset(preset_key)
        if preset and "mensagem" in preset:
            msg = preset["mensagem"]
            name = preset.get("contato", "")
            if name:
                msg = msg.replace("{nome}", name).replace("{name}", name)
            return msg.replace("\\n", "\n")

    message = os.getenv("MESSAGE", "").strip()
    if not message:
        preset1 = get_preset("mensagem_1")
        if preset1 and "mensagem" in preset1:
            message = preset1["mensagem"]
        else:
            raise ValueError("A MESSAGE não foi definida no arquivo .env nem em mensagens.json.")
    
    name = get_contact_name(preset_key)
    if name:
        message = message.replace("{nome}", name).replace("{name}", name)

    return message.replace("\\n", "\n")

def get_schedule_time(preset_key: str = None) -> str:
    if preset_key:
        preset = get_preset(preset_key)
        if preset and "horario" in preset:
            return preset["horario"]
    time_str = os.getenv("SCHEDULE_TIME", "09:00").strip()
    if not re.match(r"^\d{2}:\d{2}$", time_str):
        raise ValueError(f"O formato de SCHEDULE_TIME '{time_str}' é inválido. Use o padrão HH:MM (ex: 09:00).")
    return time_str

def is_headless() -> bool:
    val = os.getenv("HEADLESS", "False").strip().lower()
    return val in ("true", "1", "yes", "sim")
