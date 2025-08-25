# db/redis_client.py
import os
import logging
from redis.asyncio import Redis
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        load_dotenv()
        self.redis_url = os.getenv("REDIS_URL")
        if not self.redis_url:
            logger.error("❌ REDIS_URL no está configurado en .env")
            raise ValueError("Missing environment variable: REDIS_URL")
        self.client = None

    async def initialize(self):
        """Inicializa la conexión a Redis."""
        try:
            self.client = Redis.from_url(self.redis_url, decode_responses=True)
            await self.client.ping()
            logger.info("✅ Conectado a Redis")
        except Exception as e:
            logger.error(f"❌ Error de conexión a Redis: {e}")
            raise

    async def get(self, key: str):
        """Obtiene un valor de Redis."""
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Error al obtener clave {key} de Redis: {e}")
            return None

    async def set(self, key: str, value: str, ex: int = None):
        """Establece un valor en Redis."""
        try:
            await self.client.set(key, value, ex=ex)
        except Exception as e:
            logger.error(f"Error al establecer clave {key} en Redis: {e}")

    async def close(self):
        """Cierra la conexión a Redis."""
        try:
            if self.client:
                await self.client.close()
                logger.info("✅ Conexión de Redis cerrada")
        except Exception as e:
            logger.error(f"Error al cerrar la conexión de Redis: {e}")