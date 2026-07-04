"""Gestión de la lista de bajas (opt-out).

Quien está en esta lista NUNCA debe recibir un mensaje. Es un requisito legal
en casi todas las jurisdicciones. Basta con que la persona responda una palabra
clave (BAJA, STOP, CANCELAR) para agregarla aquí.
"""
import csv
from pathlib import Path

# Palabras que, si el deudor responde, deben darlo de baja.
OPT_OUT_KEYWORDS = {"baja", "stop", "cancelar", "no", "salir", "unsubscribe"}


def load_optouts(path: str | Path) -> set[str]:
    """Devuelve el conjunto de teléfonos dados de baja."""
    p = Path(path)
    if not p.exists():
        return set()
    numbers: set[str] = set()
    with open(p, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tel = (row.get("telefono") or "").strip()
            if tel:
                numbers.add(tel)
    return numbers


def add_optout(path: str | Path, telefono: str) -> None:
    """Agrega un teléfono a la lista de bajas (sin duplicar)."""
    existing = load_optouts(path)
    if telefono in existing:
        return
    p = Path(path)
    write_header = not p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["telefono"])
        writer.writerow([telefono])


def is_optout_message(body: str) -> bool:
    """True si el texto recibido es una solicitud de baja."""
    return body.strip().lower() in OPT_OUT_KEYWORDS
