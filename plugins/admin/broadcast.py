# commands/broadcast.py
import os
import time
from dotenv import load_dotenv
from srca.configs import addCommand, Client
from db.mongo_client import MongoDB
from pyrogram.errors import RPCError

# ✅ Cargar variables de entorno
load_dotenv()

# ✅ Obtener LOG_GROUP_ID desde el archivo .env con validación
LOG_GROUP_ID = os.getenv("LOG_GROUP_ID")
if LOG_GROUP_ID is None:
    raise ValueError("LOG_GROUP_ID no está definido en el archivo .env")
try:
    LOG_GROUP_ID = int(LOG_GROUP_ID)
except ValueError:
    raise ValueError("LOG_GROUP_ID debe ser un número entero válido")

@addCommand('broadcast')
def broadcast_message(_, m):
    # Inicializar la base de datos
    try:
        db = MongoDB()
        # Verificar la conexión a MongoDB
        db.client.server_info()  # Esto lanza una excepción si la conexión falla
    except Exception as e:
        return m.reply(f"❌ Error al conectar a la base de datos: {str(e)}")

    user_id = int(m.from_user.id)

    # Verificar si el usuario está registrado
    try:
        querY = db.query_user(user_id)
        if querY is None:
            return m.reply("❌ Usa el comando /register para registrarte.")
    except Exception as e:
        return m.reply(f"❌ Error al verificar el usuario en la base de datos: {str(e)}")

    # Permitir solo Owner o Admin
    try:
        if not db.is_admin(user_id):
            return m.reply("⛔ No tienes permisos para usar este comando. Solo el Owner o Admins pueden usar este comando.")
    except Exception as e:
        return m.reply(f"❌ Error al verificar permisos en la base de datos: {str(e)}")

    # Determinar el mensaje a enviar
    message_to_send = None

    # Caso 1: Responder a un mensaje
    if m.reply_to_message:
        if m.reply_to_message.text:
            message_to_send = m.reply_to_message.text
        else:
            return m.reply("⚠️ El mensaje al que respondiste no contiene texto. Por favor, responde a un mensaje de texto o usa <code>/broadcast mensaje</code>.")

    # Caso 2: Mensaje proporcionado como argumento
    else:
        data = m.text.split(' ', 1)  # Divide el comando y el mensaje
        if len(data) < 2:
            return m.reply("⚠️ Uso incorrecto: <code>/broadcast mensaje</code>")
        message_to_send = data[1]

    # Obtener todos los usuarios registrados
    try:
        users = db.get_all_users()
        if not users:
            return m.reply("⚠️ No hay usuarios registrados en el bot.")
    except Exception as e:
        return m.reply(f"❌ Error al obtener los usuarios de la base de datos: {str(e)}")

    # Enviar mensaje a cada usuario por lotes
    successful_sends = 0
    failed_sends = 0
    failed_reasons = {}  # Para registrar las razones de los fallos
    batch_size = 20  # Procesar usuarios en lotes de 20
    batch_delay = 60  # Pausa de 60 segundos entre lotes

    for i in range(0, len(users), batch_size):
        batch = users[i:i + batch_size]
        for user in batch:
            user_id_to_send = user.get('id')
            if not user_id_to_send or not isinstance(user_id_to_send, int):
                failed_sends += 1
                failed_reasons[user_id_to_send] = "ID de usuario no válido"
                continue

            try:
                # Verificar si el usuario puede recibir mensajes
                # Esto es una verificación básica para asegurarnos de que el usuario existe
                user_info = Client.get_chat(user_id_to_send)
                if not user_info:
                    raise RPCError("No se pudo obtener información del usuario")

                # Enviar el mensaje
                Client.send_message(
                    user_id_to_send,
                    f"<b>📢 Mensaje del Owner:</b>\n{message_to_send}"
                )
                successful_sends += 1

            except RPCError as e:
                failed_sends += 1
                # Identificar el tipo de error basado en el código o mensaje
                if e.code == 420:  # FLOOD_WAIT
                    failed_reasons[user_id_to_send] = f"FloodWait: {e.message}"
                    wait_time = int(e.message.split("FLOOD_WAIT_")[1]) if "FLOOD_WAIT_" in e.message else 60
                    time.sleep(wait_time)
                    try:
                        Client.send_message(
                            user_id_to_send,
                            f"<b>📢 Mensaje del Owner:</b>\n{message_to_send}"
                        )
                        successful_sends += 1
                        failed_sends -= 1
                        del failed_reasons[user_id_to_send]
                    except RPCError as retry_e:
                        failed_reasons[user_id_to_send] = f"FloodWait reintentado: {retry_e.message}"

                elif e.code == 403 and "USER_IS_BLOCKED" in e.message:
                    failed_reasons[user_id_to_send] = "Usuario ha bloqueado al bot"

                elif e.code == 400 and "CHAT_ID_INVALID" in e.message:
                    failed_reasons[user_id_to_send] = "Chat no encontrado (usuario inactivo o eliminado)"

                elif e.code == 400 and "PEER_ID_INVALID" in e.message:
                    failed_reasons[user_id_to_send] = "ID de usuario no válido"

                else:
                    failed_reasons[user_id_to_send] = f"Error de Telegram: {e.message} (Código: {e.code})"

            except Exception as e:
                failed_sends += 1
                failed_reasons[user_id_to_send] = f"Error desconocido: {str(e)}"

            # Pausa entre envíos dentro del lote
            time.sleep(1)  # Pausa de 1 segundo entre cada envío

        # Pausa entre lotes
        if i + batch_size < len(users):
            time.sleep(batch_delay)  # Pausa de 60 segundos entre lotes

    # Formatear las razones de los fallos
    failed_summary = "\n".join([f"🆔 {user_id}: {reason}" for user_id, reason in failed_reasons.items()])

    # Enviar confirmación al owner
    m.reply(f"✅ Mensaje enviado a los usuarios.\n"
            f"📩 Enviados: {successful_sends}\n"
            f"❌ Fallidos: {failed_sends}\n"
            f"📋 Razones de los fallos:\n{failed_summary if failed_summary else 'Ninguna'}")

    # Enviar log al grupo de registros
    try:
        log_text = f"""<b>📢 Broadcast Realizado</b>
━━━━━━━━━━━━━━━━━━
👤 <b>Admin/Owner:</b> {m.from_user.first_name} (@{m.from_user.username or 'Sin usuario'})
🆔 <b>ID:</b> {m.from_user.id}
📩 <b>Mensaje:</b> {message_to_send}
📊 <b>Enviados:</b> {successful_sends}
❌ <b>Fallidos:</b> {failed_sends}
📋 <b>Razones de los fallos:</b>
{failed_summary if failed_summary else 'Ninguna'}
━━━━━━━━━━━━━━━━━━"""
        Client.send_message(LOG_GROUP_ID, log_text)
    except Exception as e:
        m.reply(f"❌ Error enviando log a {LOG_GROUP_ID}: {str(e)}")