from srca.configs import addCommand, Client
from db.mongo_client import MongoDB
import os
from dotenv import load_dotenv

# ✅ Cargar variables de entorno
load_dotenv()
LOG_USER_ID = 7389519750  # ID del usuario que recibirá los logs

@addCommand('redeem')
async def redeem(client, m):
    try:
        db = MongoDB()
        user_id = int(m.from_user.id)
        chat_id = int(m.chat.id)  # Capturar el chat donde se ejecuta el comando

        # 🔹 Verificar si el usuario está registrado
        user = db.query_user(user_id)
        if user is None:
            return await m.reply("❌ **Debes registrarte primero con /register.**")

        # 🔹 Obtener la clave ingresada
        data = m.text.split(' ')
        if len(data) < 2:
            return await m.reply("⚠️ **Uso incorrecto:** `/redeem <clave>`")

        key = data[1]
        key_data = db.query_key(key)

        # 🔹 Verificar si la clave existe
        if key_data is None:
            return await m.reply("❌ **La clave ingresada no es válida o ya fue utilizada.**")

        # 🔹 Extraer información de la clave
        dias = key_data.get("dias", 0)
        generated_by = key_data.get("generated_by", "Desconocido")  # Quién generó la clave

        if dias <= 0:
            return await m.reply("❌ **Error: La clave no tiene días válidos.**")

        # 🔹 Actualizar el usuario con los días
        db.update_user(user_id, dias)

        # 🔹 Autorizar automáticamente el chat si no está en la DB
        if db.query_group(chat_id) is None:
            db.insert_group(chat_id, dias)

        # 🔹 Eliminar la clave después del canjeo
        db.delete_key(key)

        # 🔹 Mensaje de confirmación en el chat
        texto = f"""✅ **Canjeo exitoso**
━━━━━━━━━━━━━━━━━━
🔑 **Clave:** `{key}`
📅 **Días añadidos:** `{dias}`
━━━━━━━━━━━━━━━━━━
👤 **Usuario:** {m.from_user.first_name} (@{m.from_user.username})
🆔 **ID:** `{user_id}`
💬 **Chat ID:** `{chat_id}`
👤 **Generado por:** `{generated_by}`
━━━━━━━━━━━━━━━━━━
"""
        await m.reply(texto)

        # 🔹 Log para el dueño del bot
        log_text = f"""🎟️ **Canjeo de clave registrado**
━━━━━━━━━━━━━━━━━━
👤 **Usuario:** {m.from_user.first_name} (@{m.from_user.username})
🆔 **ID:** `{user_id}`
💬 **Chat ID:** `{chat_id}`
🔑 **Clave usada:** `{key}`
📅 **Días añadidos:** `{dias}`
👤 **Clave generada por:** `{generated_by}`
━━━━━━━━━━━━━━━━━━"""

        # ✅ Enviar log privado al dueño del bot
        await client.send_message(LOG_USER_ID, log_text)

    except Exception as e:
        await m.reply(f"❌ **Error al canjear la clave:** `{e}`")