from pyrogram import filters, Client, enums
import requests, re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from db.mongo_client import MongoDB
from paquetes.luhn_ccs_gen import Generator
from datetime import datetime

def obtener_usuario(user_id):
    db = MongoDB()
    return db.query_user(user_id)

def obtener_info_bin(bin_):
    try:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_[:6]}", timeout=5)
        if response.status_code == 200 and 'Invalid BIN' not in response.text:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return None

@Client.on_message(filters.command('gen', prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)
def generar_tarjetas(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Usuario"
    argumentos = message.text.split()

    if len(argumentos) < 2:
        return message.reply("⚠️ Uso incorrecto. Formato válido: /gen <code>BIN</code> [cantidad opcional]")

    ccbin = argumentos[1]
    cantidad = int(argumentos[2]) if len(argumentos) > 2 and argumentos[2].isdigit() else 10
    cantidad = min(max(cantidad, 1), 30)

    if not re.match(r'\d{6,}', ccbin):
        return message.reply("⚠️ El BIN debe tener al menos 6 dígitos numéricos.")

    usuario = obtener_usuario(user_id)
    if not usuario:
        return message.reply("❌ Debes registrarte con /register antes de usar este comando.")
    if usuario.get('role') == 'baneado':
        return message.reply("🚫 Tu cuenta ha sido baneada y no puedes generar tarjetas.")

    bin_info = obtener_info_bin(ccbin)
    if not bin_info:
        return message.reply("❌ BIN inválido o no encontrado en la base de datos.")

    try:
        tarjetas = Generator(ccbin, cantidad, True).generate_ccs()
    except Exception as e:
        return message.reply(f"⚠️ Error al generar tarjetas: {e}")

    tarjetas_texto = '\n'.join(f"<code>{cc}</code>" for cc in tarjetas)
    texto = f"""<b>💳 Generador de Tarjetas</b>
━━━━━━━━━━━━━━━━━━
📌 <b>BIN:</b> <code>{ccbin}</code>
🔢 <b>Cantidad:</b> {cantidad} tarjetas generadas
{tarjetas_texto}
━━━━━━━━━━━━━━━━━━
🏦 <b>Información del BIN:</b>
🔹 País: {bin_info.get('country_name', 'Desconocido')} {bin_info.get('country_flag', '')}
🔹 Banco: {bin_info.get('bank', 'Desconocido')}
🔹 Tipo: {bin_info.get('type', 'Desconocido')}
🔹 Nivel: {bin_info.get('level', 'Desconocido')}
🔹 Marca: {bin_info.get('brand', 'Desconocido')}
━━━━━━━━━━━━━━━━━━
👤 <b>Generado por:</b> @{username}
"""

    botones = InlineKeyboardMarkup([[InlineKeyboardButton("Regenerar", callback_data=f"regen:{user_id}")]])
    message.reply(texto, reply_markup=botones, reply_to_message_id=message.id)

@Client.on_message(filters.command('extra', prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)
def extrapolar_tarjetas(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Usuario"
    argumentos = message.text.split()
    
    if len(argumentos) < 2:
        return message.reply("⚠️ Uso incorrecto. Formato válido: /extra <code>TARJETA_BASE</code>")

    base_cc = argumentos[1]
    if not re.match(r'\d{6,}', base_cc):
        return message.reply("⚠️ La tarjeta base debe contener al menos 6 dígitos numéricos.")

    usuario = obtener_usuario(user_id)
    if not usuario:
        return message.reply("❌ Debes registrarte con /register antes de usar este comando.")
    if usuario.get('role') == 'baneado':
        return message.reply("🚫 Tu cuenta ha sido baneada y no puedes extrapolar tarjetas.")

    try:
        extrapolaciones = Generator(base_cc, 10, True).generate_ccs()
    except Exception as e:
        return message.reply(f"⚠️ Error al extrapolar tarjetas: {e}")

    tarjetas_texto = '\n'.join(f"<code>{cc}</code>" for cc in extrapolaciones)
    texto = f"""<b>💳 Extrapolador de Tarjetas</b>
━━━━━━━━━━━━━━━━━━
📌 <b>Tarjeta Base:</b> <code>{base_cc}</code>
🔢 <b>Extrapolaciones verificadas:</b>
{tarjetas_texto}
━━━━━━━━━━━━━━━━━━
👤 <b>Generado por:</b> @{username}
"""
    message.reply(texto, reply_to_message_id=message.id)