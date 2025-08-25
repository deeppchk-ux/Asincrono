from pyrogram import Client
from pyrogram.types import CallbackQuery
import logging
import os
from dotenv import load_dotenv

# ✅ Cargar variables de entorno desde Render
load_dotenv()

class SexoBot():
    def __init__(self):
        self.app = Client(
            "SexoBot",
            session_string=os.getenv("SESSION_STRING"),  # 🔹 Usamos SESSION_STRING en lugar de las claves tradicionales
            plugins   = dict(root="plugins")
        )

        @self.app.on_callback_query()
        def clod(client, call: CallbackQuery):
            data = call.data.split(":")
            if call.from_user.id != int(data[1]):
                call.answer("🚫 Botones bloqueados.")
            else:
                call.continue_propagation()

    def runn(self):
        os.system("cls" if os.name == "nt" else "clear")  # Limpia terminal en Windows/Linux
        logging.basicConfig(level=logging.INFO)
        self.app.run()

# ✅ Ejecutar el bot
if __name__ == "__main__":
    SexoBot().runn()