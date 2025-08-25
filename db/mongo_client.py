# db/mongo_client.py
import pymongo
import os
import datetime
import time
import threading
import requests
from dotenv import load_dotenv
from bson.objectid import ObjectId

# ✅ Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
LOG_GROUP_ID = os.getenv("LOG_GROUP_ID")
if LOG_GROUP_ID is None:
    raise ValueError("LOG_GROUP_ID no está definido en el archivo .env")
try:
    LOG_GROUP_ID = int(LOG_GROUP_ID)
except ValueError:
    raise ValueError("LOG_GROUP_ID debe ser un número entero válido")

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token del bot de Telegram
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN no está definido en el archivo .env")

class MongoDB:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URI)
            self.db = self.client["sdkchk"]
            self.users = self.db["usuarios"]
            self.groups = self.db["grupos"]
            self.keys = self.db["keys"]
            self.searches = self.db["searches"]  # Nueva colección para almacenar búsquedas
            self.client.server_info()  # Verifica la conexión
            print("✅ Conectado a MongoDB Atlas")
        except Exception as e:
            print(f"❌ Error al conectar a MongoDB Atlas: {e}")

    # 🔹 Consultas de usuario, grupo y clave
    def query_user(self, user_id: int):
        return self.users.find_one({"id": user_id})

    def query_group(self, group_id: int):
        return self.groups.find_one({"id": group_id})

    def query_key(self, key: str):
        return self.keys.find_one({"key": key})

    # ✅ Gestión de Cookies de Amazon
    def save_amazon_cookie(self, user_id: int, cookie: str):
        """Guarda la cookie de Amazon en la base de datos."""
        self.users.update_one({"id": user_id}, {"$set": {"amazon_cookie": cookie}}, upsert=True)

    def get_amazon_cookie(self, user_id: int):
        """Obtiene la cookie de Amazon almacenada en la base de datos."""
        user = self.query_user(user_id)
        return user.get("amazon_cookie") if user else None

    def has_valid_amazon_cookie(self, user_id: int):
        """Verifica si el usuario tiene una cookie válida de Amazon."""
        user = self.query_user(user_id)
        return user and user.get("amazon_cookie") not in [None, ""]

    # ✅ Gestión de Créditos
    def update_credits(self, user_id: int, amount: int):
        """Añade o descuenta créditos de un usuario."""
        self.users.update_one({"id": user_id}, {"$inc": {"credits": amount}}, upsert=True)

    def get_credits(self, user_id: int):
        """Obtiene el número de créditos disponibles de un usuario."""
        user = self.query_user(user_id)
        return user.get("credits", 0)

    def has_enough_credits(self, user_id: int, required_credits: int):
        """Verifica si el usuario tiene suficientes créditos."""
        return self.get_credits(user_id) >= required_credits

    # 🔹 Obtener y guardar enlaces de invitación
    def get_invite_link(self, user_id: int):
        """Obtiene el enlace de invitación del usuario si está guardado en la base de datos."""
        user = self.query_user(user_id)
        return user.get("invite_link") if user else None

    def save_invite_link(self, user_id: int, invite_link: str):
        """Guarda o actualiza el enlace de invitación en la base de datos."""
        self.users.update_one(
            {"id": user_id},
            {"$set": {"invite_link": invite_link}},
            upsert=True
        )

    def create_invite_link(self, chat_id):
        """Crea un enlace de invitación para un grupo de Telegram."""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/createChatInviteLink"
        params = {"chat_id": chat_id}
        response = requests.post(url, json=params).json()
        return response["result"]["invite_link"] if "result" in response else None

    # 🔹 Insertar datos
    def insert_user(self, data: dict):
        self.users.insert_one(data)

    def insert_group(self, group_id: int, days: int):
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
        self.groups.insert_one({"id": group_id, "dias": expiration_time.timestamp()})

    def save_key(self, key: str, days: int):
        self.keys.insert_one({"key": key, "dias": days})

    # 🔹 Actualización de usuarios y grupos
    def update_user(self, user_id: int, days: int):
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
        self.users.update_one(
            {"id": user_id},
            {"$set": {
                "plan": "premium",
                "since": expiration_time.timestamp(),
                "antispam": 20
            }},
            upsert=True
        )

    def update_group(self, group_id: int, days: int):
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
        self.groups.update_one(
            {"id": group_id},
            {"$set": {"dias": expiration_time.timestamp()}},
            upsert=True
        )

    # 🔹 Resetear referidos SIN afectar el plan premium
    def reset_referidos(self, user_id: int):
        """Resetea el contador de referidos sin tocar el plan premium"""
        self.users.update_one(
            {"id": user_id},
            {"$set": {"referidos": 0}}
        )

    # ✅ Métodos para gestión de Premium
    def get_premium_users(self):
        """Obtiene todos los usuarios con plan Premium."""
        return list(self.users.find({"plan": "premium"}))

    def update_user_premium_expiry(self, user_id: int, new_expiry: datetime.datetime):
        """Actualiza la fecha de expiración del Premium para un usuario."""
        self.users.update_one(
            {"id": user_id},
            {"$set": {"since": new_expiry.timestamp()}},
            upsert=True
        )

    # ✅ Método para obtener todos los usuarios
    def get_all_users(self):
        """Obtiene todos los usuarios registrados en la base de datos."""
        return list(self.users.find())

    # ✅ Eliminación automática de Premium vencido
    def remove_expired_premium(self):
        """Elimina Premium de los usuarios vencidos cada 5 minutos."""
        while True:
            try:
                current_time = time.time()
                expired_users = list(self.users.find({"plan": "premium", "since": {"$lt": current_time}}))

                for user in expired_users:
                    self.users.update_one(
                        {"id": user["id"]},
                        {"$set": {"plan": "free"}, "$unset": {"since": ""}}
                    )
                    self.send_log(f"🚫 Premium removido: Usuario {user['id']} (Expirado)")

                time.sleep(300)  # Revisión cada 5 minutos
            except Exception as e:
                print(f"❌ Error en la limpieza de Premium: {e}")
                time.sleep(60)

    # 🔹 Eliminaciones
    def delete_key(self, key: str):
        self.keys.delete_one({"key": key})

    def delete_group(self, group_id: int):
        self.groups.delete_one({"id": group_id})

    # 🔹 Verificación de permisos
    def is_admin(self, user_id: int):
        user = self.query_user(user_id)
        return user and user.get("role") in ["Admin", "Owner", "Co-Owner"]

    def is_owner(self, user_id: int):
        user = self.query_user(user_id)
        return user and user.get("role") in ["Owner", "Co-Owner"]

    # 🔹 Expulsión automática de usuarios/grupos con suscripción vencida
    def expulse_user(self):
        while True:
            try:
                for group in self.groups.find({"dias": {"$lt": time.time()}}):
                    self.delete_group(group["id"])
                    self.send_log(f"🚫 Se revocó el acceso del grupo con ID {group['id']}.")

                time.sleep(30)
            except Exception as e:
                print(f"❌ Error en el proceso de expiración: {e}")
                time.sleep(10)

    def send_log(self, message: str):
        """Envía mensajes al grupo de logs"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": LOG_GROUP_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, params=params)

    # 🔹 Métodos para el comando /site
    def insert_search(self, search_data: dict):
        """Inserta una búsqueda en la base de datos y devuelve el ID"""
        result = self.searches.insert_one(search_data)
        return str(result.inserted_id)

    def get_search(self, search_id: str):
        """Obtiene una búsqueda por su ID"""
        try:
            return self.searches.find_one({"_id": ObjectId(search_id)})
        except Exception as e:
            print(f"❌ Error al obtener búsqueda {search_id}: {e}")
            return None

# ✅ Iniciar la verificación automática solo una vez
mongo_instance = MongoDB()
threading.Thread(target=mongo_instance.expulse_user, daemon=True).start()
threading.Thread(target=mongo_instance.remove_expired_premium, daemon=True).start()