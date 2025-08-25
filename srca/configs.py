import re
import random
import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.errors import FloodWait, RPCError
import logging

# Configurar logging
logger = logging.getLogger(__name__)

async def padlock(callback_query: CallbackQuery):
    """Verifica si el usuario que envía el CallbackQuery es el mismo que el mensaje original."""
    try:
        if callback_query.message.from_user.id == callback_query.from_user.id:
            return True  # Permitir que el manejador continúe
        else:
            await callback_query.answer("Comando bloqueado ‼️", show_alert=True)
            return False
    except Exception as e:
        logger.error(f"Error en padlock: {e}")
        await callback_query.answer("❌ Error verificando el comando.", show_alert=True)
        return False

def find_cards(text: str) -> tuple[str, str, str, str] | str:
    """Busca información de tarjeta de crédito en el texto."""
    try:
        card_info = re.search(r'(\d{15,16})+?[^0-9]+?(\d{1,2})[\D]*?(\d{2,4})[^0-9]+?(\d{3,4})', text)
        if card_info:
            cc, mes, ano, cvv = card_info.groups()
            cc = cc.replace("-", "").replace(" ", "")
            return cc, mes, ano, cvv
        return '<b>ingrese la ccs.</b>'
    except Exception as e:
        logger.error(f"Error en find_cards: {e}")
        return '<b>ingrese la ccs.</b>'

def add_command(command: str | list[str]):
    """Decorador para registrar comandos con múltiples prefijos."""
    prefixes = ['.', '/', ',', '¡', '-', '_', '|', '"', "'", '#', '$', '%', '&', '(', ')', '*', '+', '[', ']', ';', '<', '>', '?', '=', '¿', ':']
    return Client.on_message(filters.command(command, prefixes=prefixes))

async def rnd_prox() -> dict[str, str]:
    """Selecciona un proxy aleatorio de srca/proxy.txt de forma asíncrona."""
    try:
        async with asyncio.Lock():  # Evitar acceso concurrente al archivo
            with open("srca/proxy.txt", "r") as archivo:
                proxies = archivo.readlines()
        if not proxies:
            logger.warning("No se encontraron proxies en srca/proxy.txt")
            return {}
        ranP = random.choice(proxies).strip()
        proxy = {'http': ranP, 'https': ranP}
        return proxy
    except FileNotFoundError:
        logger.error("Archivo srca/proxy.txt no encontrado")
        return {}
    except Exception as e:
        logger.error(f"Error en rnd_prox: {e}")
        return {}

last_request_time = {}
async def antispam(tiempo: float, message: Message) -> bool:
    """Implementa un sistema de antispam basado en tiempo por usuario."""
    user_id = message.from_user.id
    current_time = time()

    try:
        if user_id in last_request_time and current_time - last_request_time[user_id] < tiempo:
            wait = int(tiempo - (current_time - last_request_time[user_id]))
            for attempt in range(3):  # Reintentos para manejar FloodWait
                try:
                    await message.reply(f"<b>Antispam <code>{wait}s</code> !</b>")
                    return True
                except FloodWait as e:
                    logger.warning(f"FloodWait en antispam, esperando {e.value} segundos")
                    await asyncio.sleep(e.value)
                except RPCError as e:
                    logger.error(f"Error de Telegram API en antispam (intento {attempt + 1}/3): {e}")
                    await asyncio.sleep(2 ** attempt)
            logger.error("No se pudo enviar mensaje de antispam tras reintentos")
            return True

        last_request_time[user_id] = current_time
        return False
    except Exception as e:
        logger.error(f"Error en antispam: {e}")
        return False