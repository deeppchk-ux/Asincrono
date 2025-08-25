# plugins/command/start.py
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from srca.configs import antispam, padlock

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def start_command(client: Client, message: Message):
    try:
        if not hasattr(client, 'redis') or not hasattr(client, 'mongo'):
            logger.error("Cliente no tiene atributos mongo o redis")
            await message.reply("<b>❌ Error de configuración del bot.</b>")
            return
        
        # Verificar antispam
        if await antispam(5, message, client.redis):
            return
        
        # Verificar autorización
        if not await padlock(message):
            await message.reply("<b>❌ No estás autorizado.</b>")
            return
        
        # Crear botón inline
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("start", callback_data=f"start:{message.from_user.id}")]
        ])
        
        # Responder al comando
        await message.reply(
            "<b>¡Bienvenido a SexoBot! 😈</b>\n\n"
            "Usa /cmds para ver los comandos disponibles.",
            reply_markup=button
        )
        logger.info(f"Comando /start ejecutado por user_id={message.from_user.id}")
    except Exception as e:
        logger.error(f"Error crítico al procesar /start: {e}", exc_info=True)
        await message.reply("<b>❌ Error al procesar el comando.</b>")

async def cmds_command(client: Client, message: Message):
    try:
        if not hasattr(client, 'redis') or not hasattr(client, 'mongo'):
            logger.error("Cliente no tiene atributos mongo o redis")
            await message.reply("<b>❌ Error de configuración del bot.</b>")
            return
        
        # Verificar antispam
        if await antispam(5, message, client.redis):
            return
        
        # Verificar autorización
        if not await padlock(message):
            await message.reply("<b>❌ No estás autorizado.</b>")
            return
        
        # Responder con lista de comandos
        await message.reply(
            "<b>Comandos disponibles:</b>\n\n"
            "/start - Iniciar el bot\n"
            "/cmds - Mostrar esta lista"
        )
        logger.info(f"Comando /cmds ejecutado por user_id={message.from_user.id}")
    except Exception as e:
        logger.error(f"Error crítico al procesar /cmds: {e}", exc_info=True)
        await message.reply("<b>❌ Error al procesar el comando.</b>")

def register(app: Client):
    """Registra los manejadores de comandos."""
    try:
        app.add_handler(filters.command("start")(start_command))
        app.add_handler(filters.command("cmds")(cmds_command))
        logger.info("Comandos /start y /cmds registrados correctamente")
    except Exception as e:
        logger.error(f"Error al registrar comandos: {e}", exc_info=True)