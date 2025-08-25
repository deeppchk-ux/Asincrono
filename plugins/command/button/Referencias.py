from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_callback_query(filters.regex("^refes$"))
async def gates(client, callback_query):  # Cambiado a async def
    cmds_C = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 ʀᴇɢʀᴇsᴀʀ", callback_data="start"),
            InlineKeyboardButton("❌ ᴄᴇʀʀᴀʀ", callback_data="exit")
        ]
    ])

    texto = (
        "<b>⏃ REFERENCIAS</b>\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n\n"
        "ꋊ  <b>Grupo oficial</b> 🌎\n"
        "   ➺ <a href='https://t.me/sDk_CHK'>Click to view</a>\n\n"
        "ꋊ  <b>Grupo de referencias (Telegram)</b> 💬\n"
        "   ➺ <a href='https://t.me/sDk_CHk_Refes'>Click to view</a>\n\n"
        "━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
        "• <b><a href='https://t.me/evehood1803'>@evehood1803</a></b>"
    )

    await callback_query.message.edit_text(  # Agregado await
        texto,
        reply_markup=cmds_C,
        disable_web_page_preview=True
    )