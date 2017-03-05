import telebot
from subprocess import call
from subprocess import check_output
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

# Functions
def listener(messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        if m.content_type == 'text':
            # Prints the sent message to the console
            if m.chat.type == 'private':
                print("Chat -> " + str(m.chat.first_name) +
                      " [" + str(m.chat.id) + "]: " + m.text)
            else:
                print("Group -> " + str(m.chat.title) +
                      " [" + str(m.chat.id) + "]: " + m.text)

def reproduceYoutube(link, m):
    call(["pkill", "omxplayer"])
    bot.send_message(m.chat.id, "Reproducing video!")
    call(["ytcli", link])
    bot.reply_to(m, "Video terminado")

def reproduceYoutubeInQueue(m):
    call(["pkill", "omxplayer"])
    bot.send_message(m.chat.id, "Reproducing video!")
    call(["ytcli", queue[0]])
    queue.pop(0)
    bot.reply_to(m.chat.id, "Video terminado")

def getPid(pname):
    return int(check_output(["pidof", pname]))

def isProcessAlive(pid):
    return path.exists("/proc/{}".format(pid))

# Initializing listener
bot.set_update_listener(listener)

global queue
queue = []

# Handlers

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

@bot.message_handler(commands=["q", "queue"])
def enqueue(m):
    queue.append(m.text.split(" ", 1)[1])
    bot.reply_to(m, "Video in queue!")

@bot.message_handler(commands=["showq", "showqueue"])
def showq(m):
    bot.send_message(m.chat.id, "{} videos in queue".format(len(queue)))

@bot.message_handler(commands=["stop"])
def stop(m):
    call(["pkill", "omxplayer"])
    bot.send_message(m.chat.id, "Player stopped")

@bot.message_handler(commands=['ping'])
def send_ping(m):
    bot.reply_to(m, "PONG!")

@bot.message_handler(commands=['update'])
def auto_update(message):
    if isAdmin_fromPrivate(message):
        bot.reply_to(message, "Reiniciando..\n\nPrueba algun comando en 10 segundos")
        print("Updating..")
        sys.exit()
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")

@bot.message_handler(func=lambda x: x == x)
def reproduce(m):
    reproduceYoutube(m.text, m)
    if not queue:
        reproduceYoutubeInQueue(queue[0], m)

print("Running...")
bot.polling()
