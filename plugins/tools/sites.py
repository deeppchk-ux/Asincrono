# plugins/tools/sites.py (o plugins/commands/site_command.py, dependiendo de tu estructura)
import requests
import json
import time
import logging
from srca.configs import addCommand
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db.mongo_client import MongoDB

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Diccionario para rastrear el tiempo del último comando por usuario (antispam)
last_command_time = {}

# Diccionario para caché de resultados (tecnología + búsqueda -> resultados)
result_cache = {}

# Clave API de VirusTotal
VIRUSTOTAL_API_KEY = "537d90bff7e6a228e0a2236fa8c08a2454bf653405810b4e20f24f481e5be7af"

# Número de resultados por página
RESULTS_PER_PAGE = 5

@addCommand('site')
def site_command(client, m):
    """Comando /site para buscar sitios web por tecnología y término de búsqueda"""
    db = MongoDB()

    # Verificar autorización del chat
    if db.query_group(m.chat.id) is None:
        m.reply("❌ Chat no autorizado.")
        return

    # Verificar usuario registrado
    querY = db.query_user(int(m.from_user.id))
    if querY is None:
        m.reply("⚠️ Usa el comando /register para registrarte.")
        return

    # Verificar si el usuario está baneado
    if querY.get('role') == 'baneado':
        m.reply("🚫 Usuario baneado.")
        return

    # Verificar plan del usuario
    if querY.get('plan') == 'free':
        m.reply("❌ Usuario Free, adquiera el plan: https://t.me/DashSab")
        return

    # Aplicar antispam (10 segundos)
    user_id = m.from_user.id
    current_time = time.time()
    if user_id in last_command_time and current_time - last_command_time[user_id] < 10:
        wait = int(10 - (current_time - last_command_time[user_id]))
        m.reply(f"⏳ Antispam activado, espera {wait}s antes de volver a intentarlo.")
        return

    last_command_time[user_id] = current_time
    inicio = time.time()

    # Verificar que se proporcionaron argumentos suficientes
    parameters = m.text.split()[1:]  # Dividir el mensaje en parámetros
    if len(parameters) < 2:
        m.reply("Debes proporcionar una tecnología y un término de búsqueda. Uso: /site <tecnología> <búsqueda>")
        return

    # Extraer tecnología y términos de búsqueda
    technology = parameters[0].lower()  # Normalizar en minúsculas
    search = " ".join(parameters[1:])

    # Validar entrada
    if len(technology) > 50 or len(search) > 100:
        m.reply("⚠️ Los parámetros son demasiado largos. Usa una tecnología y búsqueda más cortas.")
        return

    # Crear clave para el caché
    cache_key = f"{technology}:{search}"
    if cache_key in result_cache and (current_time - result_cache[cache_key]["timestamp"]) < 300:  # 5 minutos de caché
        data = result_cache[cache_key]["data"]
        logger.info(f"Usando caché para {cache_key}")
    else:
        # Crear mensaje inicial de procesamiento con barra de progreso
        new = m.reply(
            f"**あ Site Search ⸙**\n"
            f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
            f"**Status:** Iniciando... [□□□□□] 0% | **From:** {m.from_user.first_name}"
        )

        # Realizar la búsqueda
        url = f"https://index.woorank.com/api/data/reviews?technologies={technology}&search={search}"
        headers = {
            'authority': 'index.woorank.com',
            'accept': '*/*',
            'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
            'if-none-match': 'W/"3a40-uA8smaE3glLUXL+45pNinOfSNNY"',
            'referer': f'https://index.woorank.com/en/reviews?technologies={technology}&search={search}',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        try:
            # Actualizar barra de progreso
            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"**Status:** Consultando API... [■□□□□] 20% | **From:** {m.from_user.first_name}"
            )

            # Realizar la solicitud a la API con timeout
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Lanza una excepción si la solicitud falla

            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"**Status:** Procesando datos... [■■■□□] 60% | **From:** {m.from_user.first_name}"
            )

            data = json.loads(response.text)
            # Guardar en caché
            result_cache[cache_key] = {"data": data, "timestamp": current_time}
            logger.info(f"Solicitud exitosa para {cache_key}")

            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"**Status:** Finalizando... [■■■■■] 100% | **From:** {m.from_user.first_name}"
            )

        except requests.Timeout:
            fin = time.time()
            botones = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
                 InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
            ])
            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"- - - - - - - - - - - - - - - - - - -\n"
                f"**Status:** Error ⚠️ | **Response:** La solicitud a la API timed out\n"
                f"**Time:** {fin-inicio:0.4f}'s | **From:** {m.from_user.first_name}",
                reply_markup=botones
            )
            return
        except requests.RequestException as e:
            fin = time.time()
            botones = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
                 InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
            ])
            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"- - - - - - - - - - - - - - - - - - -\n"
                f"**Status:** Error ⚠️ | **Response:** Error en la solicitud: {str(e)}\n"
                f"**Time:** {fin-inicio:0.4f}'s | **From:** {m.from_user.first_name}",
                reply_markup=botones
            )
            return
        except json.JSONDecodeError:
            fin = time.time()
            botones = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
                 InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
            ])
            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"- - - - - - - - - - - - - - - - - - -\n"
                f"**Status:** Error ⚠️ | **Response:** Respuesta de la API no es un JSON válido\n"
                f"**Time:** {fin-inicio:0.4f}'s | **From:** {m.from_user.first_name}",
                reply_markup=botones
            )
            return

    try:
        if 'items' in data:
            # Guardar resultados en la base de datos
            search_id = db.insert_search({
                "user_id": user_id,
                "technology": technology,
                "search": search,
                "results": data.get('items', []),
                "timestamp": current_time
            })

            # Mostrar la primera página de resultados
            show_results_page(client, new, search_id, 0, technology, search, m.from_user.first_name, inicio)
        else:
            fin = time.time()
            botones = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
                 InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
            ])
            new.edit_text(
                f"**あ Site Search ⸙**\n"
                f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
                f"- - - - - - - - - - - - - - - - - - -\n"
                f"**Status:** No se encontraron resultados ❌\n"
                f"**Time:** {fin-inicio:0.4f}'s | **From:** {m.from_user.first_name}",
                reply_markup=botones
            )

    except Exception as e:
        fin = time.time()
        botones = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
             InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
        ])
        new.edit_text(
            f"**あ Site Search ⸙**\n"
            f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
            f"- - - - - - - - - - - - - - - - - - -\n"
            f"**Status:** Error ⚠️ | **Response:** {str(e)}\n"
            f"**Time:** {fin-inicio:0.4f}'s | **From:** {m.from_user.first_name}",
            reply_markup=botones
        )

def show_results_page(client, message, search_id, page, technology, search, user_name, inicio):
    """Función para mostrar una página de resultados con paginación"""
    db = MongoDB()
    search_data = db.get_search(search_id)
    if not search_data:
        message.edit_text("⚠️ Error: No se encontraron los datos de la búsqueda.")
        return

    items = search_data["results"]
    total_items = len(items)
    total_pages = (total_items + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

    if page < 0 or page >= total_pages:
        return

    start_idx = page * RESULTS_PER_PAGE
    end_idx = min(start_idx + RESULTS_PER_PAGE, total_items)
    results = []

    for idx, item in enumerate(items[start_idx:end_idx], start=start_idx + 1):
        # Extraer información del resultado
        site_url = item.get('url', 'N/A')
        title = item.get('title', 'N/A')
        score = item.get('score', 'N/A')
        country = item.get('country', 'N/A')
        technologies = item.get('technologies', [])

        # Detectar tecnologías clave
        detected_tech = []
        if "shopify" in technologies:
            detected_tech.append("Shopify")
        if "braintree" in technologies:
            detected_tech.append("Braintree")

        # Generar lista de tecnologías en formato de texto (compactada)
        tech_list = ", ".join(technologies) if technologies else "N/A"

        # Generar lista de tecnologías detectadas
        detected_tech_text = ", ".join(detected_tech) if detected_tech else "N/A"

        # Verificar si el sitio es "clean" usando VirusTotal
        safety_status = "🔄 Checking..."
        try:
            vt_scan_url = "https://www.virustotal.com/api/v3/urls"
            headers_vt = {
                "x-apikey": VIRUSTOTAL_API_KEY,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data_vt = {"url": site_url}
            scan_response = requests.post(vt_scan_url, headers=headers_vt, data=data_vt, timeout=5)
            scan_response.raise_for_status()
            scan_data = scan_response.json()
            scan_id = scan_data["data"]["id"]

            vt_analysis_url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
            analysis_response = requests.get(vt_analysis_url, headers=headers_vt, timeout=5)
            analysis_response.raise_for_status()
            analysis_data = analysis_response.json()

            stats = analysis_data["data"]["attributes"]["stats"]
            if stats["malicious"] > 0 or stats["suspicious"] > 0:
                safety_status = "⚠️ Unsafe"
            else:
                safety_status = "✅ Clean"
        except Exception as e:
            safety_status = f"❓ Error: {str(e)}"

        # Formatear la respuesta con título en negritas y resto en monoespaciado
        # Simplificamos la f-string para evitar problemas de sintaxis
        result_text = (
            f"**Sitio #{idx}**\n"
            f"**{title}**\n"
            f"```\n"
            f"URL: {site_url}\n"
            f"Puntaje: {score}\n"
            f"País: {country}\n"
            f"Tecnologías: {tech_list}\n"
            f"Clave: {detected_tech_text}\n"
            f"Seguridad: {safety_status}\n"
            f"```\n"
            f"- - - - - - - - - - - - - - - - - - -\n"
        )
        results.append(result_text)

    # Crear botones de paginación
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"site_page:{search_id}:{page-1}"))
    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"site_page:{search_id}:{page+1}"))
    buttons.append(InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"))
    buttons.append(InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24"))

    botones = InlineKeyboardMarkup([buttons] if len(buttons) == 2 else [buttons[:2], buttons[2:]])

    # Crear mensaje final con los resultados
    fin = time.time()
    final_reply = (
        f"**あ Site Search ⸙**\n"
        f"**Tecnología:** {technology} | **Búsqueda:** {search}\n"
        f"- - - - - - - - - - - - - - - - - - -\n"
        f"{''.join(results)}"
        f"(↯) Time: {fin-inicio:0.4f}'s\n"
        f"(↯) From: {user_name}"
    )

    message.edit_text(final_reply, reply_markup=botones)

@Client.on_callback_query()
def handle_pagination(client, callback_query: CallbackQuery):
    """Manejador para los botones de paginación"""
    data = callback_query.data
    if data.startswith("site_page:"):
        _, search_id, page = data.split(":")
        page = int(page)

        db = MongoDB()
        search_data = db.get_search(search_id)
        if not search_data:
            callback_query.message.edit_text("⚠️ Error: No se encontraron los datos de la búsqueda.")
            return

        technology = search_data["technology"]
        search = search_data["search"]
        user_name = callback_query.from_user.first_name
        inicio = search_data["timestamp"]

        show_results_page(client, callback_query.message, search_id, page, technology, search, user_name, inicio)
        callback_query.answer()