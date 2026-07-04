"""Pruebas mínimas de las piezas clave, sin depender de Twilio."""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.compliance import within_allowed_hours
from src.contacts import load_contacts
from src.main import render
from src.optout import is_optout_message, load_optouts

BASE = Path(__file__).resolve().parent.parent


def test_render_rellena_variables():
    out = render("Hola {nombre}, debes ${monto}", {"nombre": "Ana", "monto": "50"})
    assert out == "Hola Ana, debes $50"


def test_horario_permitido():
    assert within_allowed_hours(9, 20, datetime(2026, 7, 4, 10, 0)) is True
    assert within_allowed_hours(9, 20, datetime(2026, 7, 4, 3, 0)) is False
    assert within_allowed_hours(9, 20, datetime(2026, 7, 4, 20, 0)) is False


def test_optout_detecta_bajas():
    assert is_optout_message("BAJA") is True
    assert is_optout_message("  stop ") is True
    assert is_optout_message("gracias") is False


def test_contactos_filtran_telefono_invalido():
    contacts = load_contacts(BASE / "data" / "contactos.csv")
    assert all(c.telefono.startswith("+") for c in contacts)
    assert len(contacts) >= 1


def test_lista_bajas_se_carga():
    bajas = load_optouts(BASE / "data" / "bajas.csv")
    assert "+5215599887766" in bajas


if __name__ == "__main__":
    import subprocess

    subprocess.run([sys.executable, "-m", "pytest", __file__, "-v"])
