import time
import random
from datetime import datetime, timedelta
from db.mongo_client import MongoDB
from srca.configs import addCommand
from pyrogram.types import Message

@addCommand('extra')
async def generate_extra(client, message: Message):
    inicio = time.time()
    db = MongoDB()

    # Obtener datos del usuario
    user_data = db.query_user(message.from_user.id)
    if not user_data:
        return await message.reply("⚠️ Debes estar registrado para usar este comando.", quote=True)

    # Verificar si el usuario está baneado
    if user_data.get("role") == "ban":
        return await message.reply("⛔ Tu cuenta ha sido baneada y no puedes usar este comando.", quote=True)

    # Verificar si el grupo está autorizado
    group_data = db.query_group(message.chat.id)
    if (user_data.get("key") and user_data["key"] != "None") or group_data:
        # Verificar si la clave del usuario ha expirado
        if user_data.get("key") and user_data["key"] != "None":
            if int(user_data["key"]) < time.time():
                db.user.update_one({"id": message.from_user.id}, {"$set": {"key": "None", "plan": "Free", "antispam": 20}})
                return await message.reply("❌ Tu membresía ha expirado.", quote=True)

        # Verificar si la clave del grupo ha expirado
        if group_data and int(group_data.get("dias", 0)) < time.time():
            db.group.delete_one({"id": message.chat.id})
            return await message.reply("❌ La membresía de este grupo ha expirado.", quote=True)

    else:
        return await message.reply("⚠️ Este grupo no está autorizado para usar este bot.", quote=True)

    # Extraer BIN de la entrada del usuario
    if not message.text:
        return await message.reply("⚠️ No se recibió entrada válida.", quote=True)

    input_data = message.text.split()
    if len(input_data) < 2:
        return await message.reply("❌ Uso incorrecto. Ejemplo: <code>/extra 551507xxxxx|rnd|rnd|rnd</code>", quote=True)

    bin_input = input_data[1][:6]

    # Generar 25 combinaciones aleatorias
    extrapolated_results = []
    for _ in range(25):
        random_digits = "".join(random.choice("0123456789") for _ in range(6))
        random_month = random.randint(1, 12)
        random_year = random.randint(2024, 2035)
        extrapolated_results.append(f"<code>{bin_input}{random_digits}xxxx|{random_month:02d}|{random_year}|rnd</code>")

    # Calcular tiempo de ejecución
    tiempo = round(time.time() - inicio, 2)

    # Manejar usuario sin username
    username = message.from_user.username or "SinUsername"

    # Formatear mensaje de respuesta
    message_text = f"""<b>
🎲 Generador de Extras
━━━━━━━━━━━━━━━━━━━
</b>""" + "\n".join(extrapolated_results) + f"""<b>
━━━━━━━━━━━━━━━━━━━
BIN: <code>{bin_input}</code>
━━━━━━━━━━━━━━━━━━━
🔹 Generado por: <code>@{username}</code>
🔹 Plan: {user_data['plan']}
🔹 Tiempo de ejecución: <code>{tiempo}s</code>
━━━━━━━━━━━━━━━━━━━
</b>"""

    await message.reply(text=message_text, quote=True)