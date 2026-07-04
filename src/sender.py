"""Envío de mensajes vía Twilio (o simulación en modo dry-run)."""
from dataclasses import dataclass

from .config import Config


@dataclass
class SendResult:
    telefono: str
    ok: bool
    detail: str  # SID del mensaje si ok, o el error si falló


class Sender:
    """Envía mensajes. Si dry_run=True, solo imprime sin enviar nada."""

    def __init__(self, config: Config, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self._client = None
        if not dry_run:
            # Import diferido: solo se necesita twilio para envíos reales.
            from twilio.rest import Client

            self._client = Client(config.account_sid, config.auth_token)

    def _format_number(self, telefono: str) -> tuple[str, str]:
        """Devuelve (from, to) con el prefijo correcto según el canal."""
        if self.config.channel == "whatsapp":
            frm = self.config.from_number
            if not frm.startswith("whatsapp:"):
                frm = f"whatsapp:{frm}"
            return frm, f"whatsapp:{telefono}"
        return self.config.from_number, telefono

    def send(self, telefono: str, body: str) -> SendResult:
        if self.dry_run:
            print(f"  [DRY-RUN] -> {telefono}:\n    " + body.replace("\n", "\n    "))
            return SendResult(telefono, True, "dry-run")

        frm, to = self._format_number(telefono)
        try:
            msg = self._client.messages.create(from_=frm, to=to, body=body)
            return SendResult(telefono, True, msg.sid)
        except Exception as e:  # noqa: BLE001 - queremos capturar cualquier fallo del proveedor
            return SendResult(telefono, False, str(e))
