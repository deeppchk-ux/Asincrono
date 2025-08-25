from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pyrogram.errors

@Client.on_callback_query(filters.regex(r"^gates$"))
async def gates(client: Client, callback_query):
    cmds_B = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Auth", callback_data="auth"),
            InlineKeyboardButton("Charge", callback_data="charged"),
            InlineKeyboardButton("Mass", callback_data="mass")
        ],
        [
            InlineKeyboardButton("Ccn", callback_data="ccn"),
            InlineKeyboardButton("Amazon", callback_data="amz")
        ],
        [
            InlineKeyboardButton("𝘈𝘵𝘳𝘢𝘴", callback_data="start")
        ]
    ])

    # Verificar si el texto cambió antes de editar
    current_text = callback_query.message.text or ""
    if current_text.strip() != cmds_texto.strip():
        try:
            await callback_query.message.edit_text(
                cmds_texto,
                reply_markup=cmds_B,
                disable_web_page_preview=True
            )
        except pyrogram.errors.MessageNotModified:
            # Ignorar si el mensaje no cambió
            pass
        except Exception as e:
            await callback_query.message.reply(
                f"Error: {str(e)}",
                disable_web_page_preview=True
            )
    else:
        # Confirmar al usuario que el clic fue procesado
        await callback_query.answer("El contenido ya está actualizado.", show_alert=False)