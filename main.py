# main.py
import os
import logging
import asyncio
import struct
from time import time
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyInvalid, AuthKeyUnregistered
from pyrogram.types import CallbackQuery
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from db.mongo_client import MongoDB
from db.redis_client import RedisClient
from srca.configs import padlock

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')  # Guardar logs en archivo para producción
    ]
)
logging.getLogger("pyrogram.connection.connection").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class SexoBot:
    def __init__(self):
        load_dotenv()
        self.name = "SexoBot"
        self.session_string = os.getenv("SESSION_STRING")
        self.log_group_id = os.getenv("LOG_GROUP_ID")
        self.plugins = {"root": "plugins"}  # Carga automática de plugins
        self.rate_limit = 1 / 30  # 30 solicitudes por segundo
        self.last_request_time = 0

        # Validar variables de entorno
        if not self.session_string:
            logger.error("Missing environment variable: SESSION_STRING")
            raise ValueError("Missing environment variable: SESSION_STRING")
        if not self.log_group_id:
            logger.error("Missing environment variable: LOG_GROUP_ID")
            raise ValueError("Missing environment variable: LOG_GROUP_ID")

        # Inicializar clientes de base de datos
        self.mongo = MongoDB()
        self.redis = RedisClient()

    async def respect_rate_limit(self):
        """Asegura que las solicitudes respeten el límite de tasa de la API de Telegram."""
        current_time = time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self.last_request_time = time()

    @retry(
        retry=retry_if_exception_type(FloodWait),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        after=lambda retry_state: logger.warning(f"Retrying ({retry_state.attempt_number}/3) due to FloodWait")
    )
    async def handle_callback_query(self, client: Client, call: CallbackQuery):
        """Maneja consultas de callback con reintentos para FloodWait."""
        try:
            await padlock(call)
        except FloodWait as e:
            logger.warning(f"FloodWait detected, waiting {e.value} seconds")
            await asyncio.sleep(e.value)
            raise
        except Exception as e:
            logger.error(f"Error en handle_callback_query: {e}")
            await call.answer("❌ Error al procesar el botón.", show_alert=True)

    async def start_bot(self):
        """Inicia el bot con manejo de errores optimizado y cierre seguro."""
        logger.info(f"Starting {self.name}")
        app = None
        try:
            # Inicializar MongoDB y Redis en paralelo
            await asyncio.gather(
                self.mongo.initialize(),
                self.redis.initialize()
            )

            app = Client(
                name=self.name,
                session_string=self.session_string,
                plugins=self.plugins,
                workers=16,  # Optimizado para producción
                sleep_threshold=180  # Aumentar para manejar FloodWait
            )

            # Configurar atributos del cliente
            app.mongo = self.mongo
            app.redis = self.redis
            app.respect_rate_limit = self.respect_rate_limit

            async with app:
                app.add_handler(
                    pyrogram.handlers.CallbackQueryHandler(self.handle_callback_query)
                )
                if app.is_connected:
                    logger.warning("Client is already connected. Attempting to reconnect...")
                    await app.stop()
                await app.start()
                logger.info(f"{self.name} is running")
                await asyncio.Event().wait()  # Mantener el bot ejecutándose
        except (ValueError, struct.error) as e:
            logger.error(f"Error deserializing SESSION_STRING: {e}. Generate a new SESSION_STRING with generate_session.py and update .env")
            raise
        except (AuthKeyInvalid, AuthKeyUnregistered) as e:
            logger.error(f"Invalid or unregistered session: {e}. Generate a new SESSION_STRING with generate_session.py and update .env")
            raise
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            # Cierre seguro de recursos
            if app and hasattr(app, 'is_connected') and app.is_connected:
                await app.stop()
                logger.info(f"{self.name} stopped gracefully")
            await asyncio.gather(
                self.mongo.close(),
                self.redis.close(),
                return_exceptions=True
            )
            logger.info("All connections closed")

    def run(self):
        """Ejecuta el bot en un bucle de eventos asyncio."""
        try:
            asyncio.run(self.start_bot())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    SexoBot().run()