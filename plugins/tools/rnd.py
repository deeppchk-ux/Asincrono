import requests
from srca.configs import addCommand
from db.mongo_client import MongoDB


@addCommand('rnd')
def bin(_,m):
    if MongoDB().query_group(m.chat.id) == None: return m.reply('Chat not Authorized.')

    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    if  querY['role'] == 'baneado': return m.reply('User baneado')
        
    bins = m.text.split(' ')
    
    if len(bins) < 2: return m.reply('ingrese el pais')
    
    req = requests.get(f'https://randomuser.me/api/?nat={bins[1]}&randomapi')

    dataR = req.json()['results'][0]

    text =f'''<b>[🌎] 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐜𝐢𝐨𝐧 𝐏𝐚𝐢𝐬
━━━━━━━━━━━━━━━━
 • Name : <code>{dataR['name']['first']} {dataR['name']['last']}</code>
 • Street : <code>{dataR['location']['street']['name']} {dataR['location']['street']['number']}</code>
 • City : <code>{dataR['location']['city']}</code>
 • State : <code>{dataR['location']['state']}</code>
 • Zip : <code>{dataR['location']['postcode']}</code>
 • Country : {dataR['location']['country']}
━━━━━━━━━━━━━━━━</b>'''

    m.reply(text)