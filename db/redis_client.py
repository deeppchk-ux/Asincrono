# db/redis_client.py
import os
import logging
from redis.asyncio import Redis, ConnectionError
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('bot.log')]
)
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        load_dotenv()
        self.redis_url = os.getenv("REDIS_URL")
        if not self.redis_url:
            logger.error("❌ REDIS_URL no está configurado en .env")
            raise ValueError("Missing environment variable: REDIS_URL")
        self.client = None

    @retry(
        retry=retry_if_exception_type(ConnectionError),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        after=lambda retry_state: logger.warning(f"Retrying Redis connection ({retry_state.attempt_number}/3)")
    )
    async def initialize(self):
        """Inicializa la conexión a Redis con reintentos."""
        try:
            self.client = Redis.from_url(self.redis_url, decode_responses=True)
            await self.client.ping()
            logger.info("✅ Conectado a Redis")
        except ConnectionError as e:
            logger.error(f"❌ Error de conexión a Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar a Redis: {e}")
            raise

    async def get(self, key: str) -> str:
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