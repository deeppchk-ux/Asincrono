from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(filters.regex("^ccn$"))
async def gates(client, callback_query):  # Cambiado a async def, parámetro a callback_query
    cmds_B = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 ɪɴɪᴄɪᴏ", callback_data="start"),
            InlineKeyboardButton("❌ ᴄᴇʀʀᴀʀ", callback_data="exit"),
        ],
        [
            InlineKeyboardButton("🔙 ʀᴇɢʀᴇsᴀʀ", callback_data="gates"),
        ]
    ])

    texto = (
        "<b>⏃ GATEWAYS CCN</b>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n\n"
        "ꋊ  <b>B3 CCN Cargo 200 MXN</b>\n"
        "   ➺ <code>!bc cc|mm|yy|cvv</code>    🟢 <b>ON</b>\n\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        "• <b><a href='https://t.me/evehood1803'>@evehood1803</a></b>"
    )

    await callback_query.message.edit_text(  # Agregado await
        texto,
        reply_markup=cmds_B,
        disable_web_page_preview=True
    )