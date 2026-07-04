"""Carga y valida la lista de contactos desde un CSV."""
import csv
import re
from dataclasses import dataclass
from pathlib import Path

# Teléfono en formato E.164: + seguido de 8 a 15 dígitos. Ej: +5215512345678
PHONE_RE = re.compile(r"^\+\d{8,15}$")


@dataclass
class Contact:
    nombre: str
    telefono: str
    monto: str
    referencia: str

    def as_vars(self) -> dict:
        """Variables disponibles para rellenar la plantilla."""
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "monto": self.monto,
            "referencia": self.referencia,
        }


def load_contacts(path: str | Path) -> list[Contact]:
    """Lee el CSV y devuelve solo los contactos con teléfono válido.

    Columnas esperadas: nombre, telefono, monto, referencia
    """
    contacts: list[Contact] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # fila 1 = encabezado
            telefono = (row.get("telefono") or "").strip()
            if not PHONE_RE.match(telefono):
                print(f"  ⚠️  Fila {i}: teléfono inválido '{telefono}', se omite.")
                continue
            contacts.append(
                Contact(
                    nombre=(row.get("nombre") or "").strip() or "estimado cliente",
                    telefono=telefono,
                    monto=(row.get("monto") or "").strip(),
                    referencia=(row.get("referencia") or "").strip(),
                )
            )
    return contacts
