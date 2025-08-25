import asyncio
import logging
import os
from time import time
from typing import Optional
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import CallbackQuery
from asyncio import Queue
from db.mongo_client import MongoDB
from db.redis_client import RedisClient
from srca.configs import padlock, antispam, add_command

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class SexoBot:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        
        # Inicializar cliente Pyrogram
        self.app = Client(
            "SexoBot",
            session_string=os.getenv("SESSION_STRING"),
            plugins=dict(root="plugins")
        )
        
        # Inicializar MongoDB y Redis
        self.mongo = MongoDB()
        self.redis = RedisClient()
        
        # Cola para manejar comandos y callbacks
        self.command_queue = Queue()
        self.rate_limit = 1 / 30  # Límite de 30 solicitudes por segundo (Telegram API)
        self.last_request_time = 0
        self.max_retries = 3
        
        # Registrar manejadores de comandos
        self._register_handlers()

    async def respect_rate_limit(self):
        """Asegura que las solicitudes respeten el límite de tasa de la API de Telegram."""
        current_time = time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self.last_request_time = time()

    def _register_handlers(self):
        """Registra manejadores de comandos y callbacks."""
        @add_command("start")
        async def start_command(client: Client, message):
            if not await antispam(5, message):  # Antispam de 5 segundos
                user_id = message.from_user.id
                user = await self.mongo.query_user(user_id)
                if user:
                    await message.reply(f"¡Bienvenido de vuelta, usuario {user_id}!")
                else:
                    await self.mongo.insert_user({"id": user_id, "plan": "free"})
                    await message.reply("¡Bienvenido al bot! Tu cuenta ha sido registrada.")

        @self.app.on_callback_query()
        async def callback_handler(client: Client, call: CallbackQuery):
            await self.command_queue.put((call, None))

    async def process_queue(self):
        """Procesa comandos y callbacks en la cola respetando límites de tasa."""
        while True:
            callback_query, task = await self.command_queue.get()
            try:
                await self.handle_callback_query(callback_query, task)
            except Exception as e:
                logger.error(f"Error procesando cola: {e}")
            finally:
                self.command_queue.task_done()

    async def handle_callback_query(self, call: CallbackQuery, task: Optional[dict] = None):
        """Maneja CallbackQuery con reintentos y manejo de FloodWait."""
        if not await padlock(call):  # Verificar si el usuario está autorizado
            return
        
        for attempt in range(self.max_retries):
            try:
                await self.respect_rate_limit()
                data = call.data.split(":")
                user_id = int(data[1])
                
                # Ejemplo: Consultar MongoDB para verificar usuario
                user = await self.mongo.query_user(user_id)
                if not user:
                    await call.answer("Usuario no encontrado.", show_alert=True)
                    return
                
                # Ejemplo: Incrementar contador en Redis
                await self.redis.incr(f"callback_count:{user_id}")
                count = await self.redis.get(f"callback_count:{user_id}")
                
                # Responder al callback
                await call.answer(f"✅ Acción permitida. Callbacks procesados: {count}", show_alert=False)
                
                # Registrar log en MongoDB
                await self.mongo.send_log(f"Callback procesado para usuario {user_id}")
                return
            except asyncio.exceptions.CancelledError:
                logger.info("Tarea cancelada en handle_callback_query")
                raise
            except ValueError as e:
                logger.error(f"Error en formato de data: {e}")
                await call.answer("❌ Error en el formato del botón.", show_alert=True)
                return
            except self.app.FloodWait as e:
                logger.warning(f"FloodWait detectado, esperando {e.value} segundos")
                await asyncio.sleep(e.value)
            except self.app.RPCError as e:
                logger.error(f"Error de Telegram API (intento {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    await call.answer("❌ Error procesando el botón.", show_alert=True)
                await asyncio.sleep(2 ** attempt)  # Backoff exponencial
            except Exception as e:
                logger.error(f"Error inesperado: {e}")
                await call.answer("❌ Error inesperado.", show_alert=True)
                return

    async def clear_terminal(self):
        """Limpia la terminal de manera asíncrona."""
        command = "cls" if os.name == "nt" else "clear"
        process = await asyncio.create_subprocess_shell(command)
        await process.communicate()

    async def run(self):
        """Inicia el bot, MongoDB y Redis."""
        try:
            await self.clear_terminal()
            logger.info("Iniciando SexoBot...")
            
            # Inicializar MongoDB y Redis
            await self.mongo.initialize()
            await self.redis.initialize()
            self.mongo.set_pyrogram_client(self.app)
            
            # Iniciar el cliente de Pyrogram
            await self.app.start()
            logger.info("SexoBot está corriendo!")
            
            # Procesar la cola en segundo plano
            asyncio.create_task(self.process_queue())
            
            # Mantener el bot corriendo
            await self.app.idle()
        except Exception as e:
            logger.error(f"Error al iniciar el bot: {e}")
        finally:
            # Cerrar conexiones
            await self.mongo.close()
            await self.redis.close()
            await self.app.stop()
            logger.info("SexoBot detenido.")

# Ejecutar el bot
if __name__ == "__main__":
    bot = SexoBot()
    asyncio.run(bot.run())