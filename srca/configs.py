# srca/configs.py
import logging
from time import time
from functools import lru_cache
from pyrogram.types import Message, CallbackQuery
from db.mongo_client import MongoDB
from db.redis_client import RedisClient

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('bot.log')]
)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1000)  # Cache para usuarios frecuentes
async def query_user_cached(user_id: int, mongo: MongoDB) -> dict:
    """Consulta un usuario en MongoDB con caché."""
    return await mongo.query_user(user_id)

async def antispam(tiempo: float, message: Message, redis: RedisClient) -> bool:
    """Verifica si el usuario está en período de enfriamiento."""
    try:
        user_id = message.from_user.id
        key = f"antispam:{user_id}"
        current_time = time()
        last_time = await redis.get(key)
        if last_time and current_time - float(last_time) < tiempo:
            wait = int(tiempo - (current_time - float(last_time)))
            await message.reply(f"<b>Antispam <code>{wait}s</code> !</b>")
            logger.info(f"Antispam activado para user_id={user_id}, espera {wait}s")
            return True
        await redis.set(key, current_time, ex=int(tiempo))
        return False
    except Exception as e:
        logger.error(f"Error en antispam para user_id={message.from_user.id}: {e}")
        return False

async def padlock(message: Message | CallbackQuery) -> bool:
    """Verifica si el usuario está autorizado."""
    try:
        user_id = message.from_user.id
        if not hasattr(message._client, 'mongo'):
            logger.error(f"Cliente no tiene atributo mongo para user_id={user_id}")
            return False
        mongo: MongoDB = message._client.mongo
        user = await query_user_cached(user_id, mongo)  # Usar caché
        if not user:
            logger.warning(f"Usuario no encontrado: user_id={user_id}")
            return False
        role = user.get("role", "user")
        plan = user.get("plan", "free")
        authorized = role in ["Owner", "Admin"] or plan == "premium"
        if not authorized:
            logger.warning(f"Usuario no autorizado: user_id={user_id}, role={role}, plan={plan}")
        return authorized
    except Exception as e:
        logger.error(f"Error en padlock para user_id={user_id}: {e}")
        return False