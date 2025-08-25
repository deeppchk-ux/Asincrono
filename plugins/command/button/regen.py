from pyrogram import filters,Client
import requests,re
from paquetes.luhn_ccs_gen import Generator
from pyrogram.types import ( InlineKeyboardButton,InlineKeyboardMarkup )

@Client.on_callback_query(filters.regex("regen"))
def exit(client, message):

    bins = message.message.reply_to_message.text.split('gen ')
    geneo = re.findall(r'[0-9]+',message.message.reply_to_message.text)
    binreq = requests.get(f'https://bins.antipublic.cc/bins/{bins[1][:6]}')
    if 'Invalid BIN' in binreq.text:return message.reply('<b>Status Dead ❌ | Invalid BIN.</b>')
    elif 'not found' in binreq.text:return message.reply('<b>Status Dead ❌ | not found</b>')
    else:

        extra = Generator(bins[1],10,True).generate_ccs()
    
        cc1 = extra[0]
        cc2 = extra[1]
        cc3 = extra[2]
        cc4 = extra[3]
        cc5 = extra[4]
        cc6 = extra[5]
        cc7 = extra[6]
        cc8 = extra[7]
        cc9 = extra[8]
        cc10 = extra[9]

                    
        texto= f'''<b>Generador ccs

Format: {bins[1]}

<code>{cc1}</code>
<code>{cc2}</code>
<code>{cc3}</code>
<code>{cc4}</code>
<code>{cc5}</code>
<code>{cc6}</code>
<code>{cc7}</code>
<code>{cc8}</code>
<code>{cc9}</code>
<code>{cc10}</code>
━━━━━━━━━━━━━━━━━━
• Bin Info: 
Pais: {binreq.json()['country_name']} [ {binreq.json()['country_flag']} ]
Bank: {binreq.json()['bank']} 
Data: {binreq.json()['brand']} - {binreq.json()['level']} - {binreq.json()['type']}
━━━━━━━━━━━━━━━━━━
by: @{message.from_user.username}</b>'''
        re_gen = InlineKeyboardMarkup([[InlineKeyboardButton("regen",callback_data=f"regen:{message.from_user.id}")],])

        message.edit_message_text(texto,reply_markup=re_gen)