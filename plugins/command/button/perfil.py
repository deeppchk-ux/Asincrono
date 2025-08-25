from pyrogram import Client, filters
from paquetes.plantillas import atras
from db.mongo_client import MongoDB
import datetime

@Client.on_callback_query(filters.regex("perfi"))
def perfil_cmon(client, m):
    try:
        perfil_text = '''<b>あ » Pepito Chk | Perfil

↯ » id: <code>{}</code>
↯ » Username: @{}
↯ » Name: <i>{}</i> 
↯ » Creditos: {}
↯ » Rango: {}
↯ » Plan: <i>{}</i>
↯ » Antispam: {}

━━━━━━━━━━━━━━━</b>'''
        querY = MongoDB().query_user(int(m.from_user.id))
        m.edit_message_text(perfil_text.format(m.from_user.id,m.from_user.username,m.from_user.first_name,querY['credits'],querY['role'],querY['plan'],querY['antispam']),reply_markup=atras(m.from_user.id))
    
    except:pass