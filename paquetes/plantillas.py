from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 🔹 Menú Principal con Estilo
def commd(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text='𝙂𝙖𝙩𝙚𝙒𝙖𝙮𝙨 ', callback_data=f'gates:{user_id}'),
            InlineKeyboardButton(text='𝙃𝙚𝙧𝙧𝙖𝙢𝙞𝙚𝙣𝙩𝙖𝙨 ', callback_data=f'tools:{user_id}')
        ],
        [
            InlineKeyboardButton(text='𝙋𝙚𝙧𝙛𝙞𝙡 👤', callback_data=f'perfil:{user_id}')
        ]
    ])

# 🔹 Menú de Gateways con el nuevo botón "Mass"
def gateways_menu(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=' 𝘾𝙃𝘼𝙍𝙂𝙀𝘿', callback_data=f'charged:{user_id}'),
            InlineKeyboardButton(text=' 𝘼𝙐𝙏𝙃', callback_data=f'auth:{user_id}')
        ],
        [
            InlineKeyboardButton(text=' 𝘾𝘾𝙉', callback_data=f'ccn:{user_id}'),
            InlineKeyboardButton(text=' 𝙈𝘼𝙎𝙎', callback_data=f'mass:{user_id}')  # Nuevo botón "Mass"
        ],
        [
            InlineKeyboardButton(text=' 𝘼𝙩𝙧𝙖𝙨', callback_data=f'atras_menu:{user_id}')
        ]
    ])

# 🔹 Menú de Mass con mismo estilo
def mass_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=' 𝘼𝙩𝙧𝙖𝙨', callback_data=f'gates:{user_id}')]
    ])

# 🔹 Menú de Charged con mismo estilo
def charged_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=' 𝘼𝙩𝙧𝙖𝙨', callback_data=f'gates:{user_id}')]
    ])

# 🔹 Menú de Auth con mismo estilo
def auth_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=' 𝘼𝙩𝙧𝙖𝙨', callback_data=f'gates:{user_id}')]
    ])

# 🔹 Menú de CCN con mismo estilo
def ccn_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=' 𝘼𝙩𝙧𝙖𝙨', callback_data=f'gates:{user_id}')]
    ])

# 🔹 Botón de regreso al menú principal con mismo estilo
def atras(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=' 𝘼𝙩𝙧𝙖𝙨', callback_data=f'atras:{user_id}')]
    ])

# 🔹 Texto del perfil del usuario con mismo estilo
perfil_text = '''<b>あ » 𝘿𝙚𝙚𝙥𝘾𝙃𝙆 | Perfil

↯ » ID: <code>{}</code>
↯ » Username: @{}
↯ » Name: <i>{}</i> 
↯ » Creditos: {}
↯ » Rango: {}
↯ » Plan: <i>{}</i>
↯ » Antispam: {}</b>
'''