import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot desde la variable de entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Verificar que el token exista
if not BOT_TOKEN:
    raise ValueError("No se encontró el BOT_TOKEN en el archivo .env")

# URL de la API
API_URL = "https://apis-dpchk.alwaysdata.net/apis/okura/Amazon.php"

# Headers para la petición
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://apis-dpchk.alwaysdata.net',
    'Referer': 'https://apis-dpchk.alwaysdata.net'
}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido! Usa /cookies para enviar cookies o /amz para enviar una lista de tarjetas.")

# Comando /cookies
async def cookies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("Por favor, proporciona las cookies después del comando. Ejemplo: /cookies TUS_COOKIES")
        return

    cookies_data = " ".join(args)  # Unir los argumentos en una sola cadena
    data = {"cookies": cookies_data}

    try:
        response = requests.post(API_URL, data=data, headers=headers)
        response_text = response.text
        await update.message.reply_text(f"Respuesta del servidor:\n{'-' * 50}\n{response_text}\n{'-' * 50}", disable_web_page_preview=True)
    except Exception as e:
        await update.message.reply_text(f"Error al hacer la petición: {str(e)}")

# Comando /amz
async def amz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("Por favor, proporciona la lista de tarjetas después del comando. Ejemplo: /amz 5303460030467517|08|2030|949")
        return

    lista_data = " ".join(args)  # Unir los argumentos en una sola cadena
    data = {"lista": lista_data}

    try:
        response = requests.post(API_URL, data=data, headers=headers)
        response_text = response.text
        await update.message.reply_text(f"Respuesta del servidor:\n{'-' * 50}\n{response_text}\n{'-' * 50}", disable_web_page_preview=True)
    except Exception as e:
        await update.message.reply_text(f"Error al hacer la petición: {str(e)}")

# Función principal
def main():
    # Crear la aplicación del bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Registrar los comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cookies", cookies))
    application.add_handler(CommandHandler("amz", amz))

    # Iniciar el bot
    print("Bot iniciado...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()