# db/redis_client.py
import redis.asyncio as redis
import os
import logging
import asyncio  # Importación explícita
from urllib.parse import urlparse
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError, RedisError
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

# Configuración de logging
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        load_dotenv()
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.parsed_url = urlparse(self.redis_url)
        self.client: Redis | None = None
        self._loop = None

    async def initialize(self):
        """Inicializa la conexión a Redis de forma asíncrona."""
        try:
            self.client = redis.Redis(
                host=self.parsed_url.hostname,
                port=self.parsed_url.port,
                password=self.parsed_url.password if self.parsed_url.password else None,
                username=self.parsed_url.username if self.parsed_url.username else None,
                ssl=True,  # Upstash requiere TLS
                decode_responses=True  # Maneja strings directamente
            )
            await self.client.ping()
            logger.info("✅ Conectado a Redis")
            self._loop = asyncio.get_event_loop()
        except RedisConnectionError as e:
            logger.error(f"❌ Error de conexión a Redis: {e}", exc_info=True)
            self.client = None
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar a Redis: {e}", exc_info=True)
            self.client = None
            raise

    async def close(self):
        """Cierra la conexión a Redis."""
        if self.client:
            try:
                if self._loop and not self._loop.is_closed():
                    await self.client.aclose()
                    logger.info("✅ Conexión a Redis cerrada")
                else:
                    logger.warning("⚠️ Bucle de eventos cerrado, omitiendo cierre de Redis")
            except Exception as e:
                logger.error(f"❌ Error al cerrar la conexión a Redis: {e}", exc_info=True)
            finally:
                self.client = None

    async def __aenter__(self):
        """Soporte para context manager."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del context manager."""
        await self.close()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def ping(self):
        """Verifica la conexión a Redis."""
        if not self.client:
            raise RedisConnectionError("Cliente Redis no inicializado")
        try:
            await self.client.ping()
            logger.debug("✅ Ping exitoso a Redis")
            return True
        except RedisConnectionError as e:
            logger.error(f"❌ Error al hacer ping a Redis: {e}", exc_info=True)
            raise
        except RedisError as e:
            logger.error(f"❌ Error de Redis: {e}", exc_info=True)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def set(self, key: str, value: str, ex: int = None):
        """Establece un valor en Redis con tiempo de expiración opcional."""
        if not self.client:
            raise RedisConnectionError("Cliente Redis no inicializado")
        try:
            start_time = asyncio.get_event_loop().time()
            await self.client.set(key, value, ex=ex)
            logger.info(f"✅ Valor establecido en Redis: key={key} en {asyncio.get_event_loop().time() - start_time:.2f}s")
        except RedisError as e:
            logger.error(f"❌ Error al establecer key={key}: {e}", exc_info=True)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get(self, key: str) -> str | None:
        """Obtiene un valor de Redis."""
        if not self.client:
            raise RedisConnectionError("Cliente Redis no inicializado")
        try:
            start_time = asyncio.get_event_loop().time()
            value = await self.client.get(key)
            logger.info(f"✅ Valor obtenido de Redis: key={key} en {asyncio.get_event_loop().time() - start_time:.2f}s")
            return value
        except RedisError as e:
            logger.error(f"❌ Error al obtener key={key}: {e}", exc_info=True)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def delete(self, key: str):
        """Elimina una clave de Redis."""
        if not self.client:
            raise RedisConnectionError("Cliente Redis no inicializado")
        try:
            start_time = asyncio.get_event_loop().time()
            await self.client.delete(key)
            logger.info(f"✅ Clave eliminada de Redis: key={key} en {asyncio.get_event_loop().time() - start_time:.2f}s")
        except RedisError as e:
            logger.error(f"❌ Error al eliminar key={key}: {e}", exc_info=True)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def incr(self, key: str) -> int:
        """Incrementa el valor de una clave en Redis."""
        if not self.client:
            raise RedisConnectionError("Cliente Redis no inicializado")
        try:
            start_time = asyncio.get_event_loop().time()
            value = await self.client.incr(key)
            logger.info(f"✅ Clave incrementada: key={key}, value={value} en {asyncio.get_event_loop().time() - start_time:.2f}s")
            return value
        except RedisError as e:
            logger.error(f"❌ Error al incrementar key={key}: {e}", exc_info=True)
            raise