# db/mongo_client.py
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('bot.log')]
)
logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        if not self.mongo_uri:
            logger.error("❌ MONGO_URI no está configurado en .env")
            raise ValueError("Missing environment variable: MONGO_URI")
        self.client = None
        self.db = None

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        after=lambda retry_state: logger.warning(f"Retrying MongoDB connection ({retry_state.attempt_number}/3)")
    )
    async def initialize(self):
        """Inicializa la conexión a MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client.get_database("cluster0")
            await self.client.admin.command("ping")
            logger.info("✅ Conectado a MongoDB Atlas")
        except Exception as e:
            logger.error(f"❌ Error de conexión a MongoDB: {e}")
            raise

    async def query_user(self, user_id: int) -> dict:
        """Consulta un usuario en la base de datos."""
        try:
            return await self.db.users.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"Error al consultar usuario {user_id}: {e}")
            return None

    async def send_log(self, log_message: str):
        """Envía un log a la colección de logs en MongoDB."""
        try:
            await self.db.logs.insert_one({
                "message": log_message,
                "timestamp": datetime.now(pytz.timezone('America/Chicago'))
            })
        except Exception as e:
            logger.error(f"Error al guardar log en MongoDB: {e}")

    async def close(self):
        """Cierra la conexión a MongoDB."""
        try:
            if self.client:
                self.client.close()
                logger.info("✅ Conexión a MongoDB cerrada")
        except Exception as e:
            logger.error(f"Error al cerrar la conexión a MongoDB: {e}")