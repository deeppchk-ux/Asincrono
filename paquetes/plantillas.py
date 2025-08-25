from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

def commd(user_id):
    commd = InlineKeyboardMarkup([[
                                InlineKeyboardButton(text='𝙋𝙚𝙧𝙛𝙞𝙡',callback_data=f'perfil:{user_id}'),
                                InlineKeyboardButton(text='𝙂𝙖𝙩𝙚𝙒𝙖𝙮𝙨',callback_data=f'gates:{user_id}'),],[
                                InlineKeyboardButton(text='𝙃𝙚𝙧𝙧𝙖𝙢𝙞𝙚𝙣𝙩𝙖𝙨',callback_data=f'tools:{user_id}')],
                                [
                                    InlineKeyboardButton(text='OWNER 👑',url='https://t.me/the_JokersKing'),
                                    InlineKeyboardButton(text='LUXURY CHAT',url='https://t.me/thejokersTeam')
                                ]])
    return commd


def atras(user_id):
    atras = InlineKeyboardMarkup([[InlineKeyboardButton(text='𝘼𝙩𝙧𝙖𝙨',callback_data=f'atras:{user_id}')]])
    return atras

perfil_text = '''<b>あ » Pepito Chk | Perfil

↯ » id: <code>{}</code>
↯ » Username: @{}
↯ » Name: <i>{}</i> 
↯ » Creditos: {}
↯ » Rango: {}
↯ » Plan: <i>{}</i>
↯ » Antispam: {}</b>
'''