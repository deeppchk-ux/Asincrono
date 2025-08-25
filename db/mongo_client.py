# db/mongo_client.py
import motor.motor_asyncio
import os
import datetime
import asyncio
from dotenv import load_dotenv
from bson.objectid import ObjectId
from motor.core import AgnosticClient, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import ConnectionFailure, OperationFailure
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('motor').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI no está definido en el archivo .env")

LOG_GROUP_ID = os.getenv("LOG_GROUP_ID", "7389519750")
try:
    LOG_GROUP_ID = int(LOG_GROUP_ID)
except ValueError:
    raise ValueError("LOG_GROUP_ID debe ser un número entero válido")

class MongoDB:
    def __init__(self):
        self.client: AgnosticClient = None
        self.db: AgnosticDatabase = None
        self.users: AsyncIOMotorCollection = None
        self.groups: AsyncIOMotorCollection = None
        self.keys: AsyncIOMotorCollection = None
        self.commands: AsyncIOMotorCollection = None
        self.group_commands: AsyncIOMotorCollection = None
        self.pyrogram_client = None
        self._loop = asyncio.get_event_loop()

    async def initialize(self):
        """Inicializa la conexión y crea índices."""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                MONGO_URI,
                maxPoolSize=10,
                minPoolSize=2,
                maxIdleTimeMS=10000,
                connectTimeoutMS=20000,
                socketTimeoutMS=20000,
                serverSelectionTimeoutMS=20000,
                retryWrites=True,
                retryReads=True,
                tls=True,
                tlsAllowInvalidCertificates=False
            )
            self.db = self.client["sdkchk"]
            self.users = self.db["usuarios"]
            self.groups = self.db["grupos"]
            self.keys = self.db["keys"]
            self.commands = self.db["commands"]
            self.group_commands = self.db["group_commands"]
            await self.client.admin.command('ping')  # Verificar conexión
            logger.info("✅ Conectado a MongoDB Atlas")
            await self._create_indexes()
            await self._ensure_owner_role()
            await self._clean_expired_premium_once()
            await self._clean_expired_groups_once()
            self._tasks = [
                asyncio.create_task(self._connection_monitor()),
                asyncio.create_task(self._premium_expiry_check()),
                asyncio.create_task(self._group_expiry_check())
            ]
        except ConnectionFailure as e:
            logger.error(f"❌ Error de conexión a MongoDB Atlas: {e}")
            self.client = None
            self.db = None
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar a MongoDB Atlas: {e}")
            self.client = None
            self.db = None
            raise

    async def close(self):
        """Cierra la conexión a MongoDB."""
        if hasattr(self, 'client') and self.client:
            try:
                # Cancelar tareas de monitoreo
                if hasattr(self, '_tasks'):
                    for task in self._tasks:
                        if not task.done():
                            task.cancel()
                    try:
                        await asyncio.gather(*self._tasks, return_exceptions=True)
                    except asyncio.CancelledError:
                        logger.info("Tareas de MongoDB canceladas durante el cierre")
                self.client.close()
                logger.info("✅ Conexión a MongoDB cerrada")
            except Exception as e:
                logger.error(f"❌ Error al cerrar la conexión a MongoDB: {e}")
            finally:
                self.client = None
                self.db = None
                self.users = None
                self.groups = None
                self.keys = None
                self.commands = None
                self.group_commands = None

    async def __aenter__(self):
        """Soporte para context manager."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del context manager."""
        await self.close()

    def set_pyrogram_client(self, client):
        """Configura el cliente Pyrogram."""
        self.pyrogram_client = client
        logger.info("✅ Cliente Pyrogram configurado en MongoDB")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def send_log(self, message: str):
        """Envía un mensaje de log al grupo de Telegram."""
        try:
            if self.pyrogram_client:
                await self.pyrogram_client.send_message(LOG_GROUP_ID, message, parse_mode="HTML")
                logger.info(f"✅ Log enviado: {message[:50]}...")
            else:
                logger.warning("⚠️ No se puede enviar log: Cliente Pyrogram no configurado")
        except Exception as e:
            logger.error(f"❌ Error al enviar log: {e}")

    async def _create_indexes(self):
        """Crea índices optimizados para las colecciones."""
        try:
            indexes = await self.users.index_information()
            if "id_1" not in indexes:
                duplicates = await self.users.aggregate([
                    {"$group": {"_id": "$id", "count": {"$sum": 1}, "docs": {"$push": "$$ROOT"}}},
                    {"$match": {"count": {"$gt": 1}}}
                ]).to_list(length=None)
                if duplicates:
                    logger.warning(f"Se encontraron {len(duplicates)} IDs duplicados en usuarios, eliminando...")
                    for group in duplicates:
                        docs = group["docs"]
                        docs.sort(key=lambda x: x["_id"].generation_time, reverse=True)
                        for doc in docs[1:]:
                            await self.users.delete_one({"_id": doc["_id"]})
                            logger.info(f"Eliminado documento duplicado con _id: {doc['_id']} para id: {group['_id']}")
                await self.users.create_index([("id", 1)], unique=True)
                logger.info("Índice id_1 creado en usuarios con unique=True")
            else:
                logger.info("Índice id_1 ya existe con unique=True en usuarios")

            await self.users.create_index([("plan", 1), ("since", 1)])
            await self.groups.create_index([("id", 1)])
            await self.groups.create_index("dias")
            await self.keys.create_index("key")
            await self.commands.create_index("cmd")
            await self.group_commands.create_index([("cmd", 1), ("chat_id", 1)], unique=True)
            logger.info("📈 Índices creados para optimizar consultas")
        except OperationFailure as e:
            logger.error(f"❌ Error al crear índices: {e}", exc_info=True)
            raise

    async def _ensure_owner_role(self):
        """Asegura que exista un usuario con rol 'Owner'."""
        try:
            owner = await self.users.find_one({"role": "Owner"})
            if not owner:
                logger.warning("⚠️ No se encontró un usuario con rol 'Owner'. Creando uno por defecto.")
                await self.users.update_one(
                    {"id": LOG_GROUP_ID},
                    {"$set": {
                        "role": "Owner",
                        "plan": "premium",
                        "since": (datetime.datetime.now() + datetime.timedelta(days=3650)).timestamp()
                    }},
                    upsert=True
                )
                logger.info(f"✅ Creado usuario owner con id={LOG_GROUP_ID}")
                self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al asegurar rol owner: {e}")
            raise

    async def _connection_monitor(self):
        """Monitorea la conexión a MongoDB periódicamente."""
        while True:
            try:
                await self.client.admin.command('ping')
                logger.debug("✅ Conexión a MongoDB activa")
            except ConnectionFailure as e:
                logger.error(f"❌ Conexión a MongoDB perdida: {e}")
            await asyncio.sleep(900)

    async def _clean_expired_premium_once(self):
        """Limpia usuarios premium expirados al inicio."""
        logger.info("🔄 Realizando limpieza inicial de usuarios premium expirados")
        try:
            current_time = time()
            cursor = self.users.find({"plan": "premium", "since": {"$lt": current_time}})
            count = 0
            async for user in cursor:
                user_id = user["id"]
                expiration_time = user.get("since", 0)
                logger.info(f"🚫 Expiración detectada (inicio) - Usuario: {user_id}, Expiró en: {expiration_time}")
                await self.users.update_one(
                    {"id": user_id},
                    {"$set": {"plan": "free"}, "$unset": {"since": ""}}
                )
                logger.info(f"✅ Plan cambiado a 'free' para usuario: {user_id}")
                await self.send_log(f"🚫 Premium removido: Usuario {user_id} (Expirado)")
                count += 1
            logger.debug(f"📊 Usuarios premium expirados procesados (inicio): {count}")
        except OperationFailure as e:
            logger.error(f"❌ Error en la limpieza inicial de Premium: {e}")
        except Exception as e:
            logger.error(f"❌ Error inesperado en _clean_expired_premium_once: {e}")

    async def _clean_expired_groups_once(self):
        """Limpia grupos expirados al inicio."""
        logger.info("🔄 Realizando limpieza inicial de grupos expirados")
        try:
            current_time = time()
            cursor = self.groups.find({"dias": {"$lt": current_time}})
            count = 0
            async for group in cursor:
                group_id = group["id"]
                expiration_time = group.get("dias", 0)
                logger.info(f"🚫 Expiración detectada (inicio) - Grupo: {group_id}, Expiró en: {expiration_time}")
                await self.delete_group(group_id)
                await self.send_log(f"🚫 Se revocó el acceso del grupo con ID {group_id}.")
                count += 1
            logger.debug(f"📊 Grupos expirados procesados (inicio): {count}")
        except OperationFailure as e:
            logger.error(f"❌ Error en la limpieza inicial de grupos: {e}")
        except Exception as e:
            logger.error(f"❌ Error inesperado en _clean_expired_groups_once: {e}")

    async def _premium_expiry_check(self):
        """Revisa periódicamente usuarios premium expirados."""
        while True:
            logger.info("🔄 Iniciando revisión periódica de usuarios premium expirados")
            try:
                current_time = time()
                cursor = self.users.find({"plan": "premium", "since": {"$lt": current_time}})
                count = 0
                async for user in cursor:
                    user_id = user["id"]
                    expiration_time = user.get("since", 0)
                    logger.info(f"🚫 Expiración detectada - Usuario: {user_id}, Expiró en: {expiration_time}")
                    await self.users.update_one(
                        {"id": user_id},
                        {"$set": {"plan": "free"}, "$unset": {"since": ""}}
                    )
                    logger.info(f"✅ Plan cambiado a 'free' para usuario: {user_id}")
                    await self.send_log(f"🚫 Premium removido: Usuario {user_id} (Expirado)")
                    count += 1
                logger.debug(f"📊 Usuarios premium expirados procesados: {count}")
            except OperationFailure as e:
                logger.error(f"❌ Error en la limpieza de Premium: {e}")
            except Exception as e:
                logger.error(f"❌ Error inesperado en _premium_expiry_check: {e}")
            await asyncio.sleep(900)

    async def _group_expiry_check(self):
        """Revisa periódicamente grupos expirados."""
        while True:
            logger.info("🔄 Iniciando revisión periódica de grupos expirados")
            try:
                current_time = time()
                cursor = self.groups.find({"dias": {"$lt": current_time}})
                count = 0
                async for group in cursor:
                    group_id = group["id"]
                    expiration_time = group.get("dias", 0)
                    logger.info(f"🚫 Expiración detectada - Grupo: {group_id}, Expiró en: {expiration_time}")
                    await self.delete_group(group_id)
                    await self.send_log(f"🚫 Se revocó el acceso del grupo con ID {group_id}.")
                    count += 1
                logger.debug(f"📊 Grupos expirados procesados: {count}")
            except OperationFailure as e:
                logger.error(f"❌ Error en la limpieza de grupos: {e}")
            except Exception as e:
                logger.error(f"❌ Error inesperado en _group_expiry_check: {e}")
            await asyncio.sleep(900)

    @lru_cache(maxsize=2000)
    async def query_user(self, user_id: int):
        """Consulta un usuario por ID."""
        try:
            start_time = time()
            user = await self.users.find_one({"id": user_id})
            if user and '_id' in user:
                user['_id'] = str(user['_id'])
            logger.info(f"Consulta query_user para user_id={user_id} en {time() - start_time:.2f}s")
            return user
        except OperationFailure as e:
            logger.error(f"❌ Error en query_user para user_id={user_id}: {e}")
            return None

    @lru_cache(maxsize=2000)
    async def query_group(self, group_id: int):
        """Consulta un grupo por ID."""
        try:
            start_time = time()
            group = await self.groups.find_one({"id": group_id})
            if group and '_id' in group:
                group['_id'] = str(group['_id'])
            logger.info(f"Consulta query_group para group_id={group_id} en {time() - start_time:.2f}s")
            return group
        except OperationFailure as e:
            logger.error(f"❌ Error en query_group para group_id={group_id}: {e}")
            return None

    @lru_cache(maxsize=2000)
    async def query_key(self, key: str):
        """Consulta una clave por su valor."""
        try:
            start_time = time()
            key_data = await self.keys.find_one({"key": key})
            if key_data and '_id' in key_data:
                key_data['_id'] = str(key_data['_id'])
            logger.info(f"Consulta query_key para key={key} en {time() - start_time:.2f}s")
            return key_data
        except OperationFailure as e:
            logger.error(f"❌ Error en query_key para key={key}: {e}")
            return None

    @lru_cache(maxsize=2000)
    async def query_command_status(self, cmd: str, chat_id: int = None):
        """Consulta el estado de un comando."""
        try:
            start_time = time()
            if chat_id:
                status = await self.group_commands.find_one({"cmd": cmd, "chat_id": chat_id})
            else:
                status = await self.commands.find_one({"cmd": cmd})
            if status and '_id' in status:
                status['_id'] = str(status['_id'])
            logger.info(f"Consulta query_command_status para cmd={cmd}, chat_id={chat_id} en {time() - start_time:.2f}s")
            return status
        except OperationFailure as e:
            logger.error(f"❌ Error en query_command_status para cmd={cmd}, chat_id={chat_id}: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def insert_user(self, data: dict):
        """Inserta un nuevo usuario."""
        try:
            start_time = time()
            if not isinstance(data.get("id"), int):
                raise ValueError(f"El campo 'id' debe ser un entero, recibido: {type(data.get('id'))}")
            existing = await self.users.find_one({"id": data.get("id")})
            if existing:
                logger.warning(f"Intento de insertar usuario ya existente: id={data.get('id')}")
                return
            result = await self.users.insert_one(data)
            logger.info(f"✅ Usuario insertado: {data.get('id')} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
            data['_id'] = str(result.inserted_id)
            return data
        except OperationFailure as e:
            logger.error(f"❌ Error al insertar usuario: {e}")
            raise
        except ValueError as e:
            logger.error(f"❌ Error de validación al insertar usuario: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def update_user_stats(self, user_id: int, command: str):
        """Actualiza estadísticas de uso de comandos."""
        try:
            start_time = time()
            await self.users.update_one(
                {"id": user_id},
                {"$inc": {f"stats.{command}": 1}},
                upsert=True
            )
            logger.info(f"✅ Estadísticas actualizadas para user_id={user_id}, comando={command} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al actualizar estadísticas para user_id={user_id}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def save_amazon_cookies(self, user_id: int, cookies: str):
        """Guarda cookies de Amazon para un usuario."""
        try:
            start_time = time()
            await self.users.update_one({"id": user_id}, {"$set": {"amazon_cookies": cookies}}, upsert=True)
            logger.info(f"✅ Cookies guardadas para user_id={user_id} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al guardar cookies para user_id={user_id}: {e}")
            raise

    async def get_amazon_cookies(self, user_id: int):
        """Obtiene cookies de Amazon para un usuario."""
        user = await self.query_user(user_id)
        return user.get("amazon_cookies") if user else None

    async def has_valid_amazon_cookies(self, user_id: int):
        """Verifica si un usuario tiene cookies válidas de Amazon."""
        user = await self.query_user(user_id)
        return user and user.get("amazon_cookies") not in [None, ""]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def delete_amazon_cookies(self, user_id: int):
        """Elimina cookies de Amazon para un usuario."""
        try:
            start_time = time()
            result = await self.users.update_one({"id": user_id}, {"$unset": {"amazon_cookies": ""}})
            if result.modified_count > 0:
                logger.info(f"✅ Cookies de Amazon eliminadas para user_id={user_id} en {time() - start_time:.2f}s")
            else:
                logger.info(f"ℹ️ No se encontraron cookies de Amazon para user_id={user_id}")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al eliminar cookies de Amazon para user_id={user_id}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def update_credits(self, user_id: int, amount: int):
        """Actualiza los créditos de un usuario."""
        try:
            start_time = time()
            await self.users.update_one({"id": user_id}, {"$inc": {"credits": amount}}, upsert=True)
            logger.info(f"✅ Créditos actualizados para user_id={user_id} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al actualizar créditos para user_id={user_id}: {e}")
            raise

    async def get_credits(self, user_id: int):
        """Obtiene los créditos de un usuario."""
        user = await self.query_user(user_id)
        return user.get("credits", 0) if user else 0

    async def has_enough_credits(self, user_id: int, required_credits: int):
        """Verifica si un usuario tiene suficientes créditos."""
        return await self.get_credits(user_id) >= required_credits

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def insert_group(self, group_id: int, days: int):
        """Inserta un nuevo grupo."""
        try:
            start_time = time()
            expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
            result = await self.groups.insert_one({"id": group_id, "dias": expiration_time.timestamp()})
            logger.info(f"✅ Grupo insertado: {group_id} en {time() - start_time:.2f}s")
            self.query_group.cache_clear()
            group_data = {"id": group_id, "dias": expiration_time.timestamp(), "_id": str(result.inserted_id)}
            return group_data
        except OperationFailure as e:
            logger.error(f"❌ Error al insertar grupo group_id={group_id}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def save_key(self, key_data: dict):
        """Guarda una nueva clave."""
        try:
            start_time = time()
            result = await self.keys.insert_one(key_data)
            logger.info(f"✅ Key guardada: {key_data.get('key')} en {time() - start_time:.2f}s")
            self.query_key.cache_clear()
            key_data['_id'] = str(result.inserted_id)
            return key_data
        except OperationFailure as e:
            logger.error(f"❌ Error al guardar key: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def update_user(self, user_id: int, days: float):
        """Actualiza el estado premium de un usuario."""
        try:
            start_time = time()
            if days <= 0:
                raise ValueError(f"El valor de days debe ser positivo, recibido: {days}")
            user = await self.query_user(user_id)
            current_time = datetime.datetime.now()
            base_time = current_time
            if user and user.get("plan") == "premium" and user.get("since"):
                existing_expiration = datetime.datetime.fromtimestamp(user["since"])
                if existing_expiration > current_time:
                    base_time = existing_expiration
                    logger.debug(f"Usuario {user_id} tiene premium activo hasta {existing_expiration}, acumulando días")
            new_expiration = base_time + datetime.timedelta(days=days)
            await self.users.update_one(
                {"id": user_id},
                {"$set": {
                    "plan": "premium",
                    "since": new_expiration.timestamp(),
                    "antispam": 20
                }},
                upsert=True
            )
            logger.info(f"✅ Usuario actualizado a premium: {user_id}, expira en {new_expiration} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al actualizar usuario user_id={user_id}: {e}")
            raise
        except ValueError as e:
            logger.error(f"❌ Error de validación para user_id={user_id}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def update_user_generic(self, user_id: int, updates: dict):
        """Actualiza un usuario con datos genéricos."""
        try:
            start_time = time()
            await self.users.update_one({"id": user_id}, {"$set": updates}, upsert=True)
            logger.info(f"✅ Usuario actualizado: {user_id} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al actualizar usuario user_id={user_id}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def update_group(self, group_id: int, days: int):
        """Actualiza un grupo."""
        try:
            start_time = time()
            expiration_time = datetime.datetime.now() + datetime.timedelta(days=days)
            await self.groups.update_one(
                {"id": group_id},
                {"$set": {"dias": expiration_time.timestamp()}},
                upsert=True
            )
            logger.info(f"✅ Grupo actualizado: {group_id} en {time() - start_time:.2f}s")
            self.query_group.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al actualizar grupo group_id={group_id}: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def add_role(self, user_id: int, role: str):
        """Asigna un rol a un usuario."""
        try:
            start_time = time()
            await self.users.update_one(
                {"id": user_id},
                {"$set": {"role": role}},
                upsert=True
            )
            logger.info(f"✅ Rol {role} asignado a user_id={user_id} en {time() - start_time:.2f}s")
            self.query_user.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al añadir rol para user_id={user_id}: {e}")
            raise

    async def count_keys_by_user(self, user_id: int, status: str):
        """Cuenta las claves generadas por un usuario con un estado específico."""
        try:
            start_time = time()
            count = await self.keys.count_documents({"generated_by": user_id, "status": status})
            logger.info(f"Consulta count_keys_by_user para user_id={user_id} en {time() - start_time:.2f}s")
            return count
        except OperationFailure as e:
            logger.error(f"❌ Error al contar claves para user_id={user_id}: {e}")
            return 0

    async def count_keys(self, status: str = None):
        """Cuenta las claves, opcionalmente filtradas por estado."""
        try:
            start_time = time()
            if status:
                count = await self.keys.count_documents({"status": status})
            else:
                count = await self.keys.count_documents({})
            logger.info(f"Consulta count_keys en {time() - start_time:.2f}s")
            return count
        except OperationFailure as e:
            logger.error(f"❌ Error al contar claves: {e}")
            return 0

    async def get_all_keys(self):
        """Obtiene todas las claves."""
        try:
            start_time = time()
            keys = []
            async for key in self.keys.find():
                if '_id' in key:
                    key['_id'] = str(key['_id'])
                keys.append(key)
            logger.info(f"Consulta get_all_keys en {time() - start_time:.2f}s")
            return keys
        except OperationFailure as e:
            logger.error(f"❌ Error al obtener todas las claves: {e}")
            return []

    async def get_all_user_ids(self):
        """Obtiene todos los IDs de usuarios."""
        try:
            users = []
            async for user in self.users.find({}, {"id": 1, "_id": 0}):
                if 'id' in user:
                    users.append(user['id'])
            logger.info(f"Usuarios encontrados para envío masivo: {users}")
            return users
        except Exception as e:
            logger.error(f"Error al obtener IDs de usuarios: {e}")
            return []

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def update_key(self, key: str, updates: dict):
        """Actualiza una clave."""
        try:
            start_time = time()
            await self.keys.update_one({"key": key}, {"$set": updates})
            logger.info(f"✅ Key actualizada: {key} en {time() - start_time:.2f}s")
            self.query_key.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al actualizar key={key}: {e}")
            raise

    async def get_premium_users(self):
        """Obtiene todos los usuarios premium."""
        try:
            start_time = time()
            users = []
            async for user in self.users.find({"plan": "premium"}):
                if '_id' in user:
                    user['_id'] = str(user['_id'])
                users.append(user)
            logger.info(f"Consulta get_premium_users en {time() - start_time:.2f}s")
            return users
        except OperationFailure as e:
            logger.error(f"❌ Error al obtener usuarios premium: {e}")
            return []

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def delete_group(self, group_id: int):
        """Elimina un grupo."""
        try:
            start_time = time()
            await self.groups.delete_one({"id": group_id})
            logger.info(f"✅ Grupo eliminado: {group_id} en {time() - start_time:.2f}s")
            self.query_group.cache_clear()
        except OperationFailure as e:
            logger.error(f"❌ Error al eliminar grupo group_id={group_id}: {e}")
            raise