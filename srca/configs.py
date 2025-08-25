import re
import time
import random
from pyrogram import Client, filters

def padlock(callback_query):
    if callback_query.message.from_user.id == callback_query.from_user.id:
        callback_query.continue_propagation()
    else:
        return callback_query.answer("Comando bloqueado ‼️")

def find_cards(text):
    try:
        card_info = re.search(r'(\d{15,16})+?[^0-9]+?(\d{1,2})[\D]*?(\d{2,4})[^0-9]+?(\d{3,4})', text)
        cc, mes, ano, cvv = card_info.groups()
        cc = cc.replace("-", "").replace(" ", "")
        return cc, mes, ano, cvv
    except:
        return '<b>ingrese la ccs.</b>'

def addCommand(command):
    ab = Client.on_message(filters.command(command, prefixes=['.', '/', ',', '¡', '-', '_', '|', '"', "'", '#', '$', '%', '&', '(', ')', '*', '+', '[', ']', ';', '<', '>', '?', '=', '¿', ':']))
    return ab

def rnd_prox():
    with open("srca/proxy.txt", "r") as archivo:
        proxies = archivo.readlines()
    ranP = random.choice(proxies).strip()
    proxy = {'http': ranP, 'https': ranP}
    return proxy

last_request_time = {}
def antispam(tiempo, message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_request_time and current_time - last_request_time[user_id] < tiempo:
        wait = int(tiempo - (current_time - last_request_time[user_id]))
        message.reply(f"<b>Antispam <code>{wait}s</code> !</b>")
        return True

    last_request_time[user_id] = current_time
    return False

def RandomName(tipo):
    if tipo == "username":
        return "User" + ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=6))
    elif tipo == "correo":
        return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8)) + "@example.com"
    elif tipo == "password":
        return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    else:
        return "default"

def SaveResponseHhml(response_text):
    with open("response.html", "w", encoding="utf-8") as file:
        file.write(response_text)

def CutStr(string, length):
    return string[:length] if len(string) > length else string