from srca.configs import addCommand,Client
from paquetes.plantillas import commd
from db.mongo_client import MongoDB

@addCommand('start')
def start(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))

    if  querY == None: 
        return m.reply('Usar el comando $register para el registro.')
        
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    Client.send_photo(_,chat_id=m.chat.id,photo='https://i.ibb.co/C38JxSHV/file-XSLt-JA8-F2-Y9mp-Fi-Lvj-LWLd.webp',caption=f"""<a href="https://t.me/Deep_Chk/3">↯</a> » 𝘽𝙞𝙚𝙣𝙫𝙚𝙣𝙞𝙙𝙤 𝘿𝙚𝙚𝙥𝘾𝙃𝙆 1.6 >_ 

𝘌𝘴 𝘶𝘯 𝘱𝘭𝘢𝘤𝘦𝘳 𝘮𝘳 @{m.from_user.username}, 𝘱𝘶𝘦𝘥𝘦𝘴 𝘮𝘢𝘯𝘦𝘫𝘢𝘳 𝘺 𝘤𝘰𝘯𝘰𝘤𝘦𝘳 𝘯𝘶𝘦𝘴𝘵𝘳𝘢 𝘭𝘪𝘴𝘵𝘢 𝘥𝘦 𝘎𝘢𝘵𝘦𝘸𝘢𝘺𝘴, 𝘛𝘰𝘰𝘭𝘴, 𝘊𝘰𝘮𝘮𝘢𝘯𝘥𝘴, 𝘦𝘯 𝘦𝘭 𝘢𝘱𝘢𝘳𝘵𝘢𝘥𝘰 𝘥𝘦 𝘣𝘰𝘵𝘰𝘯𝘦𝘴.
<a href="https://t.me/Deep_chk_bot">»</a><i> Mas información</i> -» <a href="https://t.me/Deep_Chk">𝘾𝙖𝙣𝙖𝙡 Of ✨</a>""",reply_markup = commd(m.from_user.id))