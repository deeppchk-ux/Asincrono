from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(filters.regex("exit"))
async def exit_callback(client, callback_query):  # Cambiado a async def
    await callback_query.answer()  # Agregado await
    await callback_query.message.delete()  # Agregado await