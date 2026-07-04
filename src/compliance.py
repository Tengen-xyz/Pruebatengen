"""Reglas de cumplimiento: horario permitido y tope de envíos."""
from datetime import datetime


def within_allowed_hours(start_hour: int, end_hour: int, now: datetime | None = None) -> bool:
    """True si la hora actual está dentro del rango permitido [start, end).

    Evita enviar mensajes de cobranza de madrugada, lo cual es ilegal o
    considerado acoso en muchas jurisdicciones.
    """
    now = now or datetime.now()
    return start_hour <= now.hour < end_hour
