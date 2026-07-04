"""Carga la configuración desde variables de entorno (.env)."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    account_sid: str
    auth_token: str
    from_number: str
    channel: str          # "sms" o "whatsapp"
    send_start_hour: int
    send_end_hour: int
    rate_limit_seconds: float
    max_per_run: int

    @classmethod
    def load(cls) -> "Config":
        return cls(
            account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
            auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
            from_number=os.getenv("TWILIO_FROM", ""),
            channel=os.getenv("CHANNEL", "sms").lower(),
            send_start_hour=int(os.getenv("SEND_START_HOUR", "9")),
            send_end_hour=int(os.getenv("SEND_END_HOUR", "20")),
            rate_limit_seconds=float(os.getenv("RATE_LIMIT_SECONDS", "1.5")),
            max_per_run=int(os.getenv("MAX_PER_RUN", "500")),
        )

    def validate(self) -> None:
        """Lanza un error claro si falta algo importante."""
        missing = [
            name
            for name, value in {
                "TWILIO_ACCOUNT_SID": self.account_sid,
                "TWILIO_AUTH_TOKEN": self.auth_token,
                "TWILIO_FROM": self.from_number,
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(
                "Faltan variables en tu .env: " + ", ".join(missing)
            )
