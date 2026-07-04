# Bot de Mensajería Masiva para Cobranza

Base de código educativa y funcional para enviar mensajes de cobranza de forma
**masiva pero responsable**: con consentimiento, opt-out automático, límites de
velocidad, horarios permitidos y registro de auditoría.

> ⚠️ **Aviso legal**: La cobranza por mensajería está regulada. Antes de usar
> esto en producción consulta las leyes de tu país (p. ej. protección de datos /
> habeas data, leyes anti-spam, normas de cobranza justa). Este proyecto te
> ayuda a cumplir, pero **no** sustituye asesoría legal.

---

## 🧠 Cómo funciona (el concepto)

Un bot de mensajería masiva son 4 piezas:

```
  [1] Lista de        [2] Plantilla         [3] Proveedor        [4] Registro
      contactos   ->      de mensaje    ->      de envío     ->      + opt-out
  (CSV/BD, con        (texto con            (Twilio, WhatsApp    (quién recibió,
   consentimiento)     variables)            Business API)        quién se dio de baja)
```

1. **Contactos**: una lista de deudores con teléfono, nombre, monto, etc.
   Cada uno debe tener consentimiento y no estar en la lista de bajas.
2. **Plantilla**: un texto con variables (`{nombre}`, `{monto}`) que se rellena
   por cada contacto.
3. **Proveedor**: el servicio que realmente entrega el mensaje. Aquí usamos
   **Twilio** (SMS y WhatsApp) porque es el más común y tiene modo de prueba.
4. **Registro y opt-out**: guardamos qué se envió y respetamos a quien pide baja.

---

## 🚀 Puesta en marcha

```bash
# 1. Instala dependencias
pip install -r requirements.txt

# 2. Copia y completa tus credenciales
cp .env.example .env
#    edita .env con tus datos de Twilio

# 3. Prueba SIN enviar nada (modo simulación)
python -m src.main --dry-run

# 4. Cuando estés listo, envía de verdad
python -m src.main
```

Empieza **siempre** con `--dry-run`: imprime en pantalla lo que enviaría, sin
gastar dinero ni molestar a nadie.

---

## 📁 Estructura

| Archivo | Qué hace |
|---|---|
| `src/main.py` | Orquesta todo: lee contactos, filtra bajas, envía, registra |
| `src/sender.py` | Habla con Twilio (o simula el envío en dry-run) |
| `src/contacts.py` | Carga y valida la lista de contactos |
| `src/optout.py` | Gestiona la lista de bajas (quién NO debe recibir mensajes) |
| `src/compliance.py` | Reglas: horario permitido, rate limit, tope diario |
| `src/config.py` | Lee la configuración desde `.env` |
| `data/contactos.csv` | Ejemplo de lista de deudores |
| `data/bajas.csv` | Lista de teléfonos dados de baja |
| `templates/recordatorio.txt` | Ejemplo de plantilla de mensaje |

---

## 📲 ¿Qué proveedor usar?

| Proveedor | Bueno para | Notas |
|---|---|---|
| **Twilio SMS** | Empezar rápido | Fácil, funciona en todos los teléfonos |
| **Twilio WhatsApp** | Volumen y mejor tasa de lectura | Requiere plantillas pre-aprobadas |
| **WhatsApp Cloud API (Meta)** | Escala grande | Más barato a volumen, setup más complejo |

Este código usa Twilio. Cambiar de proveedor solo requiere reescribir
`src/sender.py` — el resto queda igual.

---

## ✅ Buenas prácticas incluidas

- **Opt-out automático**: nadie en `data/bajas.csv` recibe mensajes.
- **Horario permitido**: no envía fuera del rango configurado (`SEND_START_HOUR`/`SEND_END_HOUR`).
- **Rate limit**: pausa entre mensajes para no saturar ni ser marcado como spam.
- **Tope diario**: límite de mensajes por corrida.
- **Registro de auditoría**: cada envío queda en `logs/`.
- **Dry-run**: prueba sin enviar.
