from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(filters.regex("^mass$"))
async def gates_massive(client, callback_query):  # Cambiado a async def, parámetro a callback_query
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Inicio", callback_data="start")],
        [
            InlineKeyboardButton("🔙 Regresar", callback_data="gates"),
            InlineKeyboardButton("❌ Cerrar", callback_data="exit"),
        ]
    ])

    texto = (
        "<b>⏃ GATEWAYS MASSIVE</b>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n\n"
        "ꋊ  <b>Massive Paypal</b>  <i>(Premium)</i>\n"
        "   ➺ <code>!mp [MAX 10]</code>    🟢 <b>ON</b>\n\n"
        "ꋊ  <b>Massive Payflow</b>  <i>(Premium)</i>\n"
        "   ➺ <code>!pf [MAX 10]</code>    🟢 <b>ON</b>\n\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        "• <b><a href='https://t.me/evehood1803'>@evehood1803</a></b>"
    )

    await callback_query.message.edit_text(  # Agregado await
        texto,
        reply_markup=kb,
        disable_web_page_preview=True
    )