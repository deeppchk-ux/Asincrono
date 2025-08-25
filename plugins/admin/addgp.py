import os
from dotenv import load_dotenv  # Para leer variables de entorno
from srca.configs import addCommand, Client
from db.mongo_client import MongoDB

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Obtener LOG_GROUP_ID desde el archivo .env
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID"))

@addCommand('addg')
def add_group(_, m):
    db = MongoDB()
    user_id = int(m.from_user.id)

    querY = db.query_user(user_id)
    if querY is None:
        return m.reply("❌ Usa el comando /register para registrarte.")

    # Permitir solo Admin o Owner
    if not db.is_admin(user_id):
        return m.reply("⛔ No tienes permisos para usar este comando.")

    data = m.text.split(' ')
    if len(data) < 3:
        return m.reply("⚠️ Uso incorrecto: <code>/addg id días</code>")

    group_id = int(data[1])
    days = int(data[2])

    if db.query_group(group_id) is None:
        db.insert_group(group_id, days)
        m.reply(f"✅ El grupo con ID {group_id} fue autorizado por {days} días.")

        log_text = f"""<b>✅ Nuevo Grupo Autorizado</b>
━━━━━━━━━━━━━━━━━━
👤 <b>Admin:</b> {m.from_user.first_name} (@{m.from_user.username})
🆔 <b>ID:</b> {m.from_user.id}
📢 <b>Grupo ID:</b> {group_id}
📅 <b>Días Autorizados:</b> {days}
━━━━━━━━━━━━━━━━━━"""

        # ✅ Enviar log al grupo de registros
        Client.send_message(LOG_GROUP_ID, log_text)
    else:
        return m.reply("⚠️ Este grupo ya tiene acceso.")