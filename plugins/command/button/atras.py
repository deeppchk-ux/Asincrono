from pyrogram import Client, filters
from paquetes.plantillas import commd

@Client.on_callback_query(filters.regex("atras"))
def atras(client, m):
    m.edit_message_text(f"""<a href="https://t.me/DuluxeChk_Bot">↯</a> » 𝘽𝙞𝙚𝙣𝙫𝙚𝙣𝙞𝙙𝙤 PepitoBot 1.6 >_ 

𝘌𝘴 𝘶𝘯 𝘱𝘭𝘢𝘤𝘦𝘳 𝘮𝘳 @{m.from_user.username}, 𝘱𝘶𝘦𝘥𝘦𝘴 𝘮𝘢𝘯𝘦𝘫𝘢𝘳 𝘺 𝘤𝘰𝘯𝘰𝘤𝘦𝘳 𝘯𝘶𝘦𝘴𝘵𝘳𝘢 𝘭𝘪𝘴𝘵𝘢 𝘥𝘦 𝘎𝘢𝘵𝘦𝘸𝘢𝘺𝘴, 𝘛𝘰𝘰𝘭𝘴, 𝘊𝘰𝘮𝘮𝘢𝘯𝘥𝘴, 𝘦𝘯 𝘦𝘭 𝘢𝘱𝘢𝘳𝘵𝘢𝘥𝘰 𝘥𝘦 𝘣𝘰𝘵𝘰𝘯𝘦𝘴.
<a href="https://t.me/DuluxeChk_Bot">»</a><i> Mas información</i> -» <a href="https://t.me/DuluxeChk_Bot">𝘾𝙖𝙣𝙖𝙡 Of ✨</a>""",reply_markup=commd(m.from_user.id))