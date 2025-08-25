# plugins/command/start.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from srca.configs import antispam, padlock
from datetime import datetime
import pytz
import logging
from pyrogram.errors import FloodWait, RPCError
import asyncio

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# =========================
# Config
# =========================
GATES_TOTAL = 38
TOOLS_TOTAL = 27
MAIN_GROUP = "@Deep_Chk_CHATT"
BRAND_HANDLE = "https://t.me/Deep_Chk_CHATT"
SYMBOL_A = '⏃'
SYMBOL_B = '➺'
MX_TZ = pytz.timezone('America/Mexico_City')
IMAGE_URL = "https://i.ibb.co/N6CKphYT/IMG-20250823-120607-666.jpg"  # Nueva URL de la imagen

# Textos por defecto para casos no registrados o baneados
REGISTRE_TEXT = "⚠️ Tu cuenta no está registrada. Usa /start para registrarte."
BAN_TEXT = "🚫 Estás baneado y no puedes usar este bot."

# Función para determinar el saludo según la hora
def dia():
    hour = datetime.now(MX_TZ).hour
    if hour < 12:
        return "Buenos días ⛅️"
    elif 12 <= hour < 17:
        return "Buenas tardes ☀️"
    elif 17 <= hour < 19:
        return "Buenas noches 🌅"
    else:
        return "Buenas noches 🌃"

# Plantilla para /start
def start_text(username: str) -> str:
    now = datetime.now(MX_TZ)
    time_str = now.strftime("%H:%M")
    saludo = dia()
    return (
        f"<b>{SYMBOL_A} {saludo}</b>\n"
        f"━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        f"{SYMBOL_B} <b>Bienvenido</b>: @{username}\n"
        f"{SYMBOL_B} <b>Hora</b>: {time_str} MX [🇲🇽]\n"
        f"{SYMBOL_B} <b>Grupo principal</b>: {MAIN_GROUP}\n\n"
        f"➺ <b>Comandos</b>: Usa /cmds para ver los comandos disponibles\n"
        f"━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        f"• <b><a href='{BRAND_HANDLE}'>DeepCHK</a></b>"
    )

# Plantilla para /cmds
def cmds_text() -> str:
    return (
        f"<b>{SYMBOL_A} COMANDOS DISPONIBLES</b>\n"
        f"━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        f"{SYMBOL_B} <b>Gateways totales</b>: <b>{GATES_TOTAL}</b> ✔️\n"
        f"{SYMBOL_B} <b>Tools totales</b>: <b>{TOOLS_TOTAL}</b> ✔️\n\n"
        f"➺ <b>Secciones</b>: Presiona los botones para explorar\n"
        f"━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        f"• <b><a href='{BRAND_HANDLE}'>DeepCHK</a></b>"
    )

# Botones para el menú principal
def main_menu_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(" Gateways", callback_data="gates"),
            InlineKeyboardButton(" Tools", callback_data="tools")
        ],
        [
            InlineKeyboardButton(" Api", callback_data="refes")
        ]
    ])

@filters.command(["start", "iniciar", "partir", "star"])
async def start_command(client: Client, message: Message):
    """Maneja el comando /start."""
    try:
        if not hasattr(client, 'mongo') or not hasattr(client, 'redis'):
            logger.error("Cliente no tiene atributos mongo o redis")
            await message.reply("<b>❌ Error de configuración del bot.</b>", disable_web_page_preview=True)
            return

        if await antispam(5, message, client.redis):  # Antispam de 5 segundos
            return

        mongo = client.mongo
        queryU = await mongo.query_user(message.from_user.id)

        if queryU is None:
            await message.reply(REGISTRE_TEXT, disable_web_page_preview=True)
            return
        if queryU.get('role') == 'Baneado':
            await message.reply(BAN_TEXT, disable_web_page_preview=True)
            return

        for attempt in range(3):
            try:
                await client.respect_rate_limit()
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=IMAGE_URL,
                    caption=start_text(message.from_user.username or "usuario"),
                    reply_markup=main_menu_buttons(),
                    reply_to_message_id=message.id,
                    disable_notification=True
                )
                await mongo.send_log(f"Comando /start ejecutado por usuario {message.from_user.id}")
                return
            except FloodWait as e:
                logger.warning(f"FloodWait detectado en start_command, esperando {e.value} segundos")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.error(f"Error de Telegram API en start_command (intento {attempt + 1}/3): {e}", exc_info=True)
                if attempt == 2:
                    await message.reply("❌ Error al procesar el comando. Inténtalo de nuevo.", disable_web_page_preview=True)
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Error inesperado en start_command: {e}", exc_info=True)
                await message.reply("❌ Error inesperado al procesar el comando.", disable_web_page_preview=True)
                return
    except Exception as e:
        logger.error(f"Error crítico en start_command: {e}", exc_info=True)
        await message.reply("❌ Error crítico al procesar el comando.", disable_web_page_preview=True)

@filters.command(["cmds", "help", "comandos", "cmd", "pasarelas", "gate", "gates", "gaterways", "gateways"])
async def cmds_command(client: Client, message: Message):
    """Maneja el comando /cmds."""
    try:
        if not hasattr(client, 'mongo') or not hasattr(client, 'redis'):
            logger.error("Cliente no tiene atributos mongo o redis")
            await message.reply("<b>❌ Error de configuración del bot.</b>", disable_web_page_preview=True)
            return

        if await antispam(5, message, client.redis):  # Antispam de 5 segundos
            return

        mongo = client.mongo
        queryU = await mongo.query_user(message.from_user.id)

        if queryU is None:
            await message.reply(REGISTRE_TEXT, disable_web_page_preview=True)
            return
        if queryU.get('role') == 'Baneado':
            await message.reply(BAN_TEXT, disable_web_page_preview=True)
            return

        for attempt in range(3):
            try:
                await client.respect_rate_limit()
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=IMAGE_URL,
                    caption=cmds_text(),
                    reply_markup=main_menu_buttons(),
                    reply_to_message_id=message.id,
                    disable_notification=True
                )
                await mongo.send_log(f"Comando /cmds ejecutado por usuario {message.from_user.id}")
                return
            except FloodWait as e:
                logger.warning(f"FloodWait detectado en cmds_command, esperando {e.value} segundos")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.error(f"Error de Telegram API en cmds_command (intento {attempt + 1}/3): {e}", exc_info=True)
                if attempt == 2:
                    await message.reply("❌ Error al procesar el comando. Inténtalo de nuevo.", disable_web_page_preview=True)
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Error inesperado en cmds_command: {e}", exc_info=True)
                await message.reply("❌ Error inesperado al procesar el comando.", disable_web_page_preview=True)
                return
    except Exception as e:
        logger.error(f"Error crítico en cmds_command: {e}", exc_info=True)
        await message.reply("❌ Error crítico al procesar el comando.", disable_web_page_preview=True)

@filters.regex("^start$")
async def start_callback(client: Client, callback_query: CallbackQuery):
    """Maneja el callback 'start'."""
    try:
        if not hasattr(client, 'mongo') or not hasattr(client, 'redis'):
            logger.error("Cliente no tiene atributos mongo o redis")
            await callback_query.answer("❌ Error de configuración del bot.", show_alert=True)
            return

        if not await padlock(callback_query):  # Verificar autorización
            return

        for attempt in range(3):
            try:
                await client.respect_rate_limit()
                # Enviar un nuevo mensaje con la imagen
                await client.send_photo(
                    chat_id=callback_query.message.chat.id,
                    photo=IMAGE_URL,
                    caption=start_text(callback_query.from_user.username or "usuario"),
                    reply_markup=main_menu_buttons(),
                    disable_notification=True
                )
                # Eliminar el mensaje anterior
                await callback_query.message.delete()
                await client.mongo.send_log(f"Callback 'start' procesado por usuario {callback_query.from_user.id}")
                return
            except FloodWait as e:
                logger.warning(f"FloodWait detectado en start_callback, esperando {e.value} segundos")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.error(f"Error de Telegram API en start_callback (intento {attempt + 1}/3): {e}", exc_info=True)
                if attempt == 2:
                    await callback_query.answer("❌ Error al procesar el botón.", show_alert=True)
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Error inesperado en start_callback: {e}", exc_info=True)
                await callback_query.answer("❌ Error inesperado al procesar el botón.", show_alert=True)
                return
    except Exception as e:
        logger.error(f"Error crítico en start_callback: {e}", exc_info=True)
        await callback_query.answer("❌ Error crítico al procesar el botón.", show_alert=True)