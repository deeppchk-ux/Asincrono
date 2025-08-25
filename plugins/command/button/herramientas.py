from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(filters.regex("^tools$"))
async def gates(client, callback_query):  # Cambiado a async def, parámetro a callback_query
    cmds_C = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 ʀᴇɢʀᴇsᴀʀ", callback_data="start"),
            InlineKeyboardButton("❌ ᴄᴇʀʀᴀʀ", callback_data="exit"),
        ]
    ])

    texto = (
        "<b>⏃ HERRAMIENTAS | TOOLS</b>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n\n"
        "ꋊ  <b>Generador BIN</b>\n"
        "   ➺ <code>!gen BIN</code>    🟢 <b>Disponible</b>\n\n"
        "ꋊ  <b>Ver tu ID</b>\n"
        "   ➺ <code>!id</code>    🟢 <b>Disponible</b>\n\n"
        "ꋊ  <b>Canjear key</b>\n"
        "   ➺ <code>!redeem key</code>    🟢 <b>Disponible</b>\n\n"
        "ꋊ  <b>Ver sellers</b>\n"
        "   ➺ <code>!seller</code>    🟢 <b>Disponible</b>\n\n"
        "ꋊ  <b>Tu información</b>\n"
        "   ➺ <code>!my</code>    🟢 <b>Disponible</b>\n\n"
        "ꋊ  <b>País aleatorio</b>\n"
        "   ➺ <code>!rnd MX,US,CA</code>    🟢 <b>Disponible</b>\n\n"
        "ꋊ  <b>Consultar precios</b>\n"
        "   ➺ <code>!precios</code>    🟢 <b>Disponible</b>\n\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        "• <i>Tip:</i> Usa los comandos en chats autorizados."
    )

    await callback_query.message.edit_text(  # Agregado await
        texto,
        reply_markup=cmds_C,
        disable_web_page_preview=True
    )