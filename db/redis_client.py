import redis
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

try:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    parsed_url = urlparse(redis_url)
    redis_client = redis.Redis(
        host=parsed_url.hostname,
        port=parsed_url.port,
        password=parsed_url.password if parsed_url.password else None,
        username=parsed_url.username if parsed_url.username else None,
        ssl=True,  # Upstash requiere TLS
        decode_responses=True  # Maneja strings directamente
    )
    redis_client.ping()
    logger.info("✅ Conectado a Redis")
except Exception as e:
    logger.error(f"❌ Error al conectar a Redis: {e}")
    redis_client = None