from srca.configs import addCommand

@addCommand(['id','ichat','idchat','idc','idg','idgp'])
def start(_,m):
    m.reply(f'id: <code>{m.from_user.id}</code>\nchat: <code>{m.chat.id}</code>')