from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(filters.regex("^charged$"))
async def gates(client, callback_query):  # Cambiado a async def, parámetro a callback_query
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 Inicio", callback_data="start"),
            InlineKeyboardButton("✖️ Cerrar", callback_data="exit"),
        ],
        [
            InlineKeyboardButton("↩️ Regresar", callback_data="gates"),
        ]
    ])

    texto = (
        "<b>⏃ GATEWAYS CHARGED</b>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n\n"
        "ꋊ  <b>Stripe Cargo 150 MXN</b>\n"
        "   ➺ <code>!sa cc|mm|yy|cvv</code>    🟢 <b>ON</b>\n\n"
        "ꋊ  <b>Payflow Cargo 400 MXN</b>\n"
        "   ➺ <code>!pw cc|mm|yy|cvv</code>    🔴 <b>OFF</b>\n\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        "• <b><a href='https://t.me/evehood1803'>@evehood1803</a></b>"
    )

    await callback_query.message.edit_text(  # Agregado await
        texto,
        reply_markup=kb,
        disable_web_page_preview=True
    )