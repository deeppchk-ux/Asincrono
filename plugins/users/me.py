from srca.configs import addCommand, Client
from paquetes.plantillas import perfil_text
from db.mongo_client import MongoDB
import datetime

@addCommand(['me', 'info', 'yo', 'perfil'])
def start(_, m):
    if MongoDB().query_group(m.chat.id) == None:
        return m.reply('Chat not Authorized.')

    querY = MongoDB().query_user(int(m.from_user.id))

    if querY == None:
        return m.reply('Usar el comando $register para el registro.')

    try:
        tiempo = datetime.datetime.fromtimestamp(querY['since'])

        data = f'<code>{tiempo.day}/{tiempo.month}/{tiempo.year}</code>'

        perfil_texta = perfil_text.format(m.from_user.id, m.from_user.username, m.from_user.first_name,
                                          querY['credits'], querY['role'], querY['plan'], querY['antispam'], data)

        m.reply_text(perfil_texta)

    except:
        perfilt = '''<b>あ » 𝘿𝙚𝙚𝙥𝘾𝙃𝙆 | Perfil

↯ » id: <code>{}</code>
↯ » Username: @{}
↯ » Name: <i>{}</i> 
↯ » Creditos: {}
↯ » Rango: {}
↯ » Plan: <i>{}</i>
↯ » Antispam: {}

━━━━━━━━━━━━━━━</b>'''
        perfil_texta = perfilt.format(m.from_user.id, m.from_user.username, m.from_user.first_name,
                                      querY['credits'], querY['role'], querY['plan'], querY['antispam'])

        m.reply_text(perfil_texta)