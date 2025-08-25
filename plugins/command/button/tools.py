from pyrogram import Client, filters
from paquetes.plantillas import atras

@Client.on_callback_query(filters.regex("tools"))
def tool_com(client, m):
    m.edit_message_text('''<b>🔧 𝙃𝙚𝙧𝙧𝙖𝙢𝙞𝙚𝙣𝙩𝙖𝙨 - Opciones Disponibles

📌 𝘾𝙤𝙢𝙖𝙣𝙙𝙤𝙨 𝙂𝙧𝙖𝙩𝙞𝙨:

↯ » Status    » Free
↯ » Cmmd    » <code>/bin</code>
↯ » Format   » <code>/bin 456789</code>
━━
↯ » Status    » Free
↯ » Cmmd    » <code>/gen</code>
↯ » Format   » <code>/gen 456789</code>
━━
↯ » Status    » Free
↯ » Cmmd    » <code>/rnd</code>
↯ » Format   » <code>/rnd us</code>
━━
↯ » Status    » Free
↯ » Cmmd    » <code>/extra</code>
↯ » Format   » <code>/extra</code>
━━
↯ » Status    » Free
↯ » Cmmd    » <code>/referidos</code>
↯ » Format   » <code>/referidos</code>
━━
↯ » Status    » Free
↯ » Cmmd    » <code>/redeem</code>
↯ » Format   » <code>/redeem + Clabe</code>
━━
↯ » Status    » Free
↯ » Cmmd    » <code>/kookies</code>
↯ » Format   » <code>/kookies + 
cookies Amazon</code> 

━━━━━━━━━━━</b>''', reply_markup=atras(m.from_user.id))