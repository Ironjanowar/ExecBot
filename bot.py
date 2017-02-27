import telebot
from subprocess import call
import os.path as path
import json
import sys

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

if not path.isfile("./data/admins.json"):
    with open('./data/admins.json', 'w') as adminData:
        adminData.write('[]')
        adminData.close

with open('./data/admins.json', 'r') as adminData:
    admins = json.load(adminData)
    
# Ignorar mensajes antiguos
bot.skip_pending = True

def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
    return False

@bot.message_handler(commands=["exec"])
def exec(m):
    command = m.text.split(" ", 1)[1]
    call(command.split(" "))
    bot.send_message(m.chat.id, "*{}* executed".format(m.text.split(" ", 1)[1]), parse_mode="Markdown")

@bot.message_handler(commands=["yt"])
def youtube(m):
    link = m.text.split(" ", 1)[1]
    # exec
    bot.send_message(m.chat.id, "Reproducing video!")
    # kill bot
    call(["ytcli", link])
    bot.reply_to(m, "Video terminado")

@bot.message_handler(command=['ping'])
def ping(m):
    bot.reply_to(m, "PONG!")

@bot.message_handler(commands=['update'])
def auto_update(message):
    if isAdmin_fromPrivate(message):
        bot.reply_to(message, "Reiniciando..\n\nPrueba algun comando en 10 segundos")
        print("Updating..")
        sys.exit()
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")

print("Running...")
bot.polling()
