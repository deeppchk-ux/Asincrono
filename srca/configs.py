# srca/configs.py
import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from typing import Callable, List
import logging

logger = logging.getLogger(__name__)

# Diccionario para antispam
antispam_dict = {}

async def antispam(tiempo: float, message: Message) -> bool:
    """Implementa control de antispam para comandos."""
    user_id = message.from_user.id
    current_time = time()
    if user_id in antispam_dict and current_time - antispam_dict[user_id] < tiempo:
        wait = int(tiempo - (current_time - antispam_dict[user_id]))
        await message.reply(f"<b>Antispam <code>{wait}s</code> !</b>")
        return True
    antispam_dict[user_id] = current_time
    return False

async def padlock(query: CallbackQuery) -> bool:
    """Verifica si el usuario está autorizado para ejecutar acciones."""
    try:
        # Ejemplo: Verificar si el usuario está en un grupo permitido
        # Ajusta esta lógica según tus necesidades
        return True
    except Exception as e:
        logger.error(f"Error en padlock: {e}")
        await query.answer("No estás autorizado.", show_alert=True)
        return False

def add_command(commands: List[str]) -> Callable:
    """Decorador para registrar comandos con múltiples prefijos."""
    prefixes = ['.', '/', ',', '¡', '-', '_', '|', '"', "'", '#', '$', '%', '&', '(', ')', '*', '+', '[', ']', ';', '<', '>', '?', '=', '¿', ':']
    
    def decorator(func: Callable) -> Callable:
        async def wrapper(client: Client, message: Message, bot_instance=None):
            try:
                await func(client, message, bot_instance)
            except Exception as e:
                logger.error(f"Error en comando {commands}: {e}")
                await message.reply("❌ Error al procesar el comando.")
        # Registrar el manejador con los prefijos
        Client.on_message(filters.command(commands, prefixes=prefixes))(wrapper)
        return wrapper
    return decorator