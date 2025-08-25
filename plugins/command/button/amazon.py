from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from crateres.textos_after import cmds_texto

@Client.on_callback_query(filters.regex("^amz$"))
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
        "<b>⏃ AMAZON GATES</b> <i>(MX | IT | US | CA | JP | AU)</i>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n\n"
        "ꋊ  <b>Amazon Check</b>\n"
        "   ➺ <code>!amz cc|mm|yy|cvv</code>    🟢 <b>ON</b>\n\n"
        "ꋊ  <b>Cookie Load</b>\n"
        "   ➺ <code>!cookie &lt;cookies&gt;</code>    🟢 <b>ON</b>\n\n"
        "ꋊ  <b>Stop Process</b>\n"
        "   ➺ <code>!stop</code>    🔴 <b>OFF</b>\n\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        "• <b><a href='https://t.me/evehood1803'>@evehood1803</a></b>"
    )

    await callback_query.message.edit_text(  # Agregado await
        texto,
        reply_markup=cmds_B,
        disable_web_page_preview=True
    )