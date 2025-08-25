# main.py
import asyncio
import logging
import os
from time import time
from typing import Optional
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.errors import FloodWait, RPCError
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
        self._client_started = False
        self._tasks = []
        
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
        @self.app.on_callback_query()
        async def callback_handler(client: Client, call: CallbackQuery):
            try:
                if not await padlock(call):
                    logger.warning(f"Callback no autorizado para user_id={call.from_user.id}")
                    return
                await self.command_queue.put((call, None))
            except Exception as e:
                logger.error(f"Error en callback_handler: {e}", exc_info=True)
                await call.answer("❌ Error procesando el botón.", show_alert=True)

    async def process_queue(self):
        """Procesa comandos y callbacks en la cola respetando límites de tasa."""
        while True:
            callback_query, task = await self.command_queue.get()
            try:
                await self.handle_callback_query(callback_query, task)
            except Exception as e:
                logger.error(f"Error crítico al procesar el comando en process_queue: {e}", exc_info=True)
            finally:
                self.command_queue.task_done()

    async def handle_callback_query(self, call: CallbackQuery, task: Optional[dict] = None):
        """Maneja CallbackQuery con reintentos y manejo de FloodWait."""
        for attempt in range(self.max_retries):
            try:
                await self.respect_rate_limit()
                data = call.data.split(":")
                user_id = int(data[1]) if len(data) > 1 else call.from_user.id
                
                # Consultar usuario en MongoDB
                user = await self.mongo.query_user(user_id)
                if not user:
                    await call.answer("Usuario no encontrado.", show_alert=True)
                    return
                
                # Incrementar contador en Redis
                await self.redis.incr(f"callback_count:{user_id}")
                count = await self.redis.get(f"callback_count:{user_id}")
                
                # Responder al callback
                await call.answer(f"✅ Acción permitida. Callbacks procesados: {count}", show_alert=False)
                
                # Registrar log en MongoDB
                await self.mongo.send_log(f"Callback procesado para usuario {user_id}")
                return
            except ValueError as e:
                logger.error(f"Error en formato de data: {e}", exc_info=True)
                await call.answer("❌ Error en el formato del botón.", show_alert=True)
                return
            except FloodWait as e:
                logger.warning(f"FloodWait detectado, esperando {e.value} segundos")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.error(f"Error de Telegram API (intento {attempt + 1}/{self.max_retries}): {e}", exc_info=True)
                if attempt == self.max_retries - 1:
                    await call.answer("❌ Error procesando el botón.", show_alert=True)
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Error crítico en handle_callback_query: {e}", exc_info=True)
                await call.answer("❌ Error inesperado.", show_alert=True)
                return

    async def clear_terminal(self):
        """Limpia la terminal de manera asíncrona."""
        try:
            os.environ["TERM"] = os.getenv("TERM", "xterm")
            command = "cls" if os.name == "nt" else "clear"
            process = await asyncio.create_subprocess_shell(command)
            await process.communicate()
        except Exception as e:
            logger.warning(f"No se pudo limpiar la terminal: {e}", exc_info=True)

    async def run(self):
        """Inicia el bot, MongoDB y Redis."""
        try:
            await self.clear_terminal()
            logger.info("Iniciando SexoBot...")
            
            # Inicializar MongoDB
            try:
                await self.mongo.initialize()
            except Exception as e:
                logger.error(f"No se pudo inicializar MongoDB: {e}", exc_info=True)
                raise
            
            # Inicializar Redis
            try:
                await self.redis.initialize()
            except Exception as e:
                logger.error(f"No se pudo inicializar Redis: {e}", exc_info=True)
                raise
            
            # Configurar cliente Pyrogram en MongoDB
            self.mongo.set_pyrogram_client(self.app)
            
            # Iniciar el cliente Pyrogram
            try:
                await self.app.start()
                self._client_started = True
                logger.info("SexoBot está corriendo!")
            except Exception as e:
                logger.error(f"No se pudo iniciar el cliente Pyrogram: {e}", exc_info=True)
                raise
            
            # Procesar la cola en segundo plano
            self._tasks.append(asyncio.create_task(self.process_queue()))
            
            # Mantener el bot corriendo
            try:
                while True:
                    await asyncio.sleep(3600)
            except asyncio.CancelledError:
                logger.info("Bot detenido por cancelación.")
                raise

        except Exception as e:
            logger.error(f"Error al iniciar el bot: {e}", exc_info=True)
            raise
        finally:
            tasks = self._tasks + [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            for task in tasks:
                if not task.done():
                    task.cancel()
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except asyncio.CancelledError:
                logger.info("Tareas canceladas durante el cierre")
            
            try:
                await self.mongo.close()
            except Exception as e:
                logger.error(f"Error al cerrar MongoDB: {e}", exc_info=True)
            
            try:
                await self.redis.close()
            except Exception as e:
                logger.error(f"Error al cerrar Redis: {e}", exc_info=True)
            
            if self._client_started:
                try:
                    await self.app.stop()
                    logger.info("SexoBot detenido.")
                except Exception as e:
                    logger.error(f"Error al detener el cliente Pyrogram: {e}", exc_info=True)
            else:
                logger.info("El cliente Pyrogram no se inició, omitiendo stop.")

if __name__ == "__main__":
    bot = SexoBot()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.run())
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario.")
    except Exception as e:
        logger.error(f"Error crítico al ejecutar el bot: {e}", exc_info=True)
    finally:
        tasks = [t for t in asyncio.all_tasks(loop=loop) if t is not asyncio.current_task(loop=loop)]
        for task in tasks:
            if not task.done():
                task.cancel()
        try:
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        except asyncio.CancelledError:
            logger.info("Tareas canceladas durante el cierre del bucle")
        if not loop.is_closed():
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
        logger.info("Bucle de eventos cerrado correctamente.")