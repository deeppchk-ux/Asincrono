# main.py
import os
import logging
import asyncio
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
        self.plugins = {"root": "plugins"}

        if not self.session_string:
            raise ValueError("Missing environment variable: SESSION_STRING")
        if not self.log_group_id:
            raise ValueError("Missing environment variable: LOG_GROUP_ID")

        # Inicializar MongoDB y Redis
        self.mongo = MongoDB()
        self.redis = RedisClient()

    @retry(
        retry=retry_if_exception_type(FloodWait),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        after=lambda retry_state: logger.warning(f"Retrying ({retry_state.attempt_number}/3) due to FloodWait")
    )
    async def handle_callback_query(self, client: Client, call: CallbackQuery):
        """Handle callback queries with retries for FloodWait."""
        try:
            await padlock(call)
        except FloodWait as e:
            logger.warning(f"FloodWait detected, waiting {e.value} seconds")
            await asyncio.sleep(e.value)
            raise

    async def start_bot(self):
        """Start the bot with optimized error handling and cleanup."""
        logger.info(f"Starting {self.name}")
        app = None
        try:
            # Inicializar MongoDB y Redis
            await self.mongo.initialize()
            await self.redis.initialize()

            app = Client(
                name=self.name,
                session_string=self.session_string,
                plugins=self.plugins,
                workers=16
            )

            # Configurar mongo y redis en el cliente
            app.mongo = self.mongo
            app.redis = self.redis

            async with app:
                app.add_handler(
                    pyrogram.handlers.CallbackQueryHandler(self.handle_callback_query)
                )
                if app.is_connected:
                    logger.warning("Client is already connected. Attempting to reconnect...")
                    await app.stop()
                await app.start()
                logger.info(f"{self.name} is running")
                await asyncio.Event().wait()
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
            if app and hasattr(app, 'is_connected') and app.is_connected:
                await app.stop()
                logger.info(f"{self.name} stopped gracefully")
            if self.mongo:
                await self.mongo.close()
                logger.info("MongoDB connection closed")
            if self.redis:
                await self.redis.close()
                logger.info("Redis connection closed")

    def run(self):
        """Run the bot in an asyncio event loop."""
        try:
            asyncio.run(self.start_bot())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    SexoBot().run()