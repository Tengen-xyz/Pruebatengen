"""Punto de entrada: orquesta el envío masivo de cobranza.

Uso:
    python -m src.main --dry-run     # simula, no envía
    python -m src.main               # envía de verdad
"""
import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

from .compliance import within_allowed_hours
from .config import Config
from .contacts import load_contacts
from .optout import load_optouts
from .sender import Sender

BASE = Path(__file__).resolve().parent.parent
CONTACTS_FILE = BASE / "data" / "contactos.csv"
OPTOUT_FILE = BASE / "data" / "bajas.csv"
TEMPLATE_FILE = BASE / "templates" / "recordatorio.txt"
LOG_DIR = BASE / "logs"


def render(template: str, variables: dict) -> str:
    """Rellena {variables} en la plantilla. Deja intactas las que no existan."""
    result = template
    for key, value in variables.items():
        result = result.replace("{" + key + "}", str(value))
    return result


def log_result(rows: list[dict]) -> Path:
    """Guarda un registro de auditoría de la corrida."""
    LOG_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = LOG_DIR / f"envio_{stamp}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["fecha", "telefono", "estado", "detalle"])
        writer.writeheader()
        writer.writerows(rows)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Bot de cobranza masiva")
    parser.add_argument("--dry-run", action="store_true", help="Simula sin enviar")
    args = parser.parse_args()

    config = Config.load()
    if not args.dry_run:
        config.validate()

    # Regla de horario (se salta en dry-run para poder probar a cualquier hora)
    if not args.dry_run and not within_allowed_hours(
        config.send_start_hour, config.send_end_hour
    ):
        print(
            f"⛔ Fuera del horario permitido "
            f"({config.send_start_hour}:00–{config.send_end_hour}:00). "
            "No se envía nada."
        )
        return 1

    contacts = load_contacts(CONTACTS_FILE)
    optouts = load_optouts(OPTOUT_FILE)
    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    # Filtra a quienes se dieron de baja: requisito legal.
    targets = [c for c in contacts if c.telefono not in optouts]
    skipped = len(contacts) - len(targets)

    print(f"📋 Contactos válidos: {len(contacts)}")
    print(f"🚫 Excluidos por baja: {skipped}")
    print(f"📤 A enviar: {min(len(targets), config.max_per_run)}")
    print(f"🔧 Canal: {config.channel} | Modo: {'DRY-RUN' if args.dry_run else 'REAL'}\n")

    sender = Sender(config, dry_run=args.dry_run)
    rows = []
    sent = 0

    for contact in targets:
        if sent >= config.max_per_run:
            print(f"\n🛑 Tope de {config.max_per_run} alcanzado. Fin.")
            break

        body = render(template, contact.as_vars())
        result = sender.send(contact.telefono, body)
        rows.append(
            {
                "fecha": datetime.now().isoformat(timespec="seconds"),
                "telefono": result.telefono,
                "estado": "OK" if result.ok else "ERROR",
                "detalle": result.detail,
            }
        )
        if result.ok:
            sent += 1
        else:
            print(f"  ❌ {contact.telefono}: {result.detail}")

        # Rate limit: pausa entre mensajes (no aplica en dry-run).
        if not args.dry_run:
            time.sleep(config.rate_limit_seconds)

    log_path = log_result(rows)
    ok_count = sum(1 for r in rows if r["estado"] == "OK")
    print(f"\n✅ Enviados OK: {ok_count} / {len(rows)}")
    print(f"📝 Registro guardado en: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
