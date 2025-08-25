from srca.configs import addCommand,Client
from db.mongo_client import MongoDB

@addCommand('register')
def start(_,m):
    try:
        querY = MongoDB().query_user(int(m.from_user.id))
    #    if  querY['role'] == 'baneado': return m.reply('User baneado')

        if  querY == None:
            data = {'id': int(m.from_user.id),'plan': 'free','role': 'user','credits': 0,'antispam': 40,'since': None}
            MongoDB().insert_user(data)

            texto= f'''<b>New User 

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}</b>'''
            Client.send_message(_,chat_id=-1002467873059,text=texto)
            
            return m.reply_text(f'Welcome {m.from_user.first_name}, acabas de registrarte ✳️.')
        
        else: m.reply('<b>Ya estas registrado.</b>')
    except: m.reply('<b>Ya estas registrado.</b>')

