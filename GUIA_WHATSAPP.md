# Guía paso a paso: tu primer WhatsApp con el Sandbox de Twilio

Objetivo: enviar tu **primer mensaje real de WhatsApp a tu propio teléfono**
usando este bot, sin esperar aprobaciones de Meta y sin gastar (el Sandbox es
gratis para pruebas).

> 🧪 **¿Qué es el Sandbox?** Un entorno de pruebas de Twilio con un número de
> WhatsApp compartido (`+1 415 523 8886`). Sirve para probar tu código HOY.
> Solo puede enviar a teléfonos que **se hayan unido** al sandbox (por eso es
> seguro: no puedes molestar a nadie que no haya aceptado). Para producción
> real luego pides tu número propio y plantillas aprobadas.

---

## Paso 1 · Crea tu cuenta de Twilio

1. Entra a <https://www.twilio.com/try-twilio> y regístrate (es gratis).
2. Verifica tu correo y tu número de teléfono.
3. Al entrar a la consola, Twilio te da crédito de prueba automáticamente.

---

## Paso 2 · Copia tus credenciales

En el **Dashboard** de la consola (<https://console.twilio.com>) verás:

| Dato | Cómo se ve | Va en `.env` como |
|---|---|---|
| Account SID | `ACxxxxxxxx...` | `TWILIO_ACCOUNT_SID` |
| Auth Token | (oculto, dale "Show") | `TWILIO_AUTH_TOKEN` |

> 🔒 El Auth Token es como tu contraseña. Nunca lo subas a GitHub. El archivo
> `.gitignore` de este proyecto ya protege tu `.env`.

---

## Paso 3 · Activa el Sandbox de WhatsApp

1. En la consola, ve al menú:
   **Messaging → Try it out → Send a WhatsApp message**
   (o directo: <https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn>)
2. Verás una instrucción como esta:

   > Para unirte, envía **`join <dos-palabras>`** al número
   > **+1 415 523 8886** desde tu WhatsApp.

   Ejemplo: `join silver-tiger` (cada cuenta tiene su frase).
3. **Desde tu WhatsApp personal**, agrega ese número y envíale exactamente ese
   texto (`join silver-tiger`).
4. Twilio te responderá confirmando que estás conectado al sandbox. ✅

Ahora tu teléfono puede **recibir** mensajes del sandbox durante 72 horas
(luego solo repites el `join`).

---

## Paso 4 · Configura tu `.env`

En la carpeta del proyecto:

```bash
cp .env.example .env
```

Edita `.env` y déjalo así (con tus datos reales):

```ini
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_auth_token_real
TWILIO_FROM=whatsapp:+14155238886      # número del sandbox, NO lo cambies
CHANNEL=whatsapp
SEND_START_HOUR=0                        # 0-24 para poder probar a cualquier hora
SEND_END_HOUR=24
RATE_LIMIT_SECONDS=1.5
MAX_PER_RUN=5
```

> El `whatsapp:+14155238886` es el número del sandbox. En producción será tu
> número propio.

---

## Paso 5 · Pon TU teléfono como único contacto

Edita `data/contactos.csv` y deja solo tu número (formato E.164, con `+` y país):

```csv
nombre,telefono,monto,referencia
Tu Nombre,+5215512345678,100.00,PRUEBA-001
```

> Reemplaza `+5215512345678` por tu número real. México = `+52`, más el número
> a 10 dígitos. Verifica que sea el **mismo** teléfono que hizo el `join`.

Asegúrate de que tu número **no** esté en `data/bajas.csv` (si está, bórralo).

---

## Paso 6 · Prueba primero en seco (dry-run)

```bash
python -m src.main --dry-run
```

Debe imprimir tu mensaje ya rellenado, sin enviar nada. Si se ve bien, sigue.

---

## Paso 7 · ¡Envía de verdad!

```bash
python -m src.main
```

En segundos deberías recibir el WhatsApp en tu teléfono. 🎉

Revisa también el registro que se creó:

```bash
ls logs/
```

Verás un `envio_AAAAMMDD_HHMMSS.csv` con el estado `OK` y el SID del mensaje.

---

## Si algo falla

| Mensaje / síntoma | Causa probable | Solución |
|---|---|---|
| `Faltan variables en tu .env` | No completaste el `.env` | Revisa Paso 4 |
| Error `63007` o "not a valid channel" | `TWILIO_FROM` sin `whatsapp:` | Debe ser `whatsapp:+14155238886` |
| No llega el mensaje | No hiciste `join`, o pasaron 72h | Repite el Paso 3 |
| Error `21608` (sandbox) | El teléfono destino no se unió al sandbox | El número de destino también debe hacer `join` |
| Teléfono "inválido, se omite" | Formato incorrecto en el CSV | Usa `+` país y número, sin espacios |

---

## Lo que sigue (cuando ya funcione el sandbox)

En el sandbox **solo** puedes enviar a números que hicieron `join`. Eso NO sirve
para cobrar a clientes reales. El siguiente nivel es:

1. **Solicitar un número de WhatsApp Business propio** (WhatsApp Sender) en Twilio.
2. **Registrar tus plantillas** de cobranza y esperar la aprobación de Meta
   (usa tu `templates/recordatorio.txt` como borrador; categoría *Utility*).
3. Cambiar `TWILIO_FROM` en `.env` por tu número propio.

El código del bot **no cambia** — solo cambias la configuración. Ese es el punto
de haberlo construido así.
