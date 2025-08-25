from srca.configs import addCommand, Client
from db.mongo_client import MongoDB
from random import randrange

@addCommand('creditos')
async def bin(_, m):
    db = MongoDB()
    user_id = int(m.from_user.id)
    querY = db.query_user(user_id)

    if querY is None:
        return await m.reply('❌ Usa el comando /register para registrarte.')

    # 🔹 Verificación de permisos (Owner, Co-Owner, Admin)
    if querY.get("role") not in ["Owner", "Co-Owner", "Admin"]:
        return await m.reply("⛔ No tienes permisos para modificar créditos.")

    data = m.text.split(' ')

    if len(data) < 3:
        return await m.reply("⚠️ Ingrese los datos correctamente. Ejemplo: /creditos id cantidad")

    try:
        idw = int(data[1])
        creditos = int(data[2])
    except ValueError:
        return await m.reply("⚠️ Asegúrate de ingresar valores numéricos válidos.")

    db.add_credits(idw, creditos)
    await m.reply("✅ Se han editado los créditos del usuario correctamente.")

    # 🔹 Registro del cambio en el grupo de Staff
    log_text = f"""<b>
🔹 Créditos Modificados
━━━━━━━━━━━━━━━━━━━ 
👤 Usuario: {m.from_user.first_name} (@{m.from_user.username})
🆔 ID: {user_id}
🎯 Modificó Créditos de:
   🔹 ID Usuario: <code>{idw}</code>
   💰 Créditos Añadidos: <code>{creditos}</code>
━━━━━━━━━━━━━━━━━━━
</b>"""

    await Client.send_message(_, chat_id=-1002467873059, text=log_text)