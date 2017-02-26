import telebot
from subprocess import call

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Ignorar mensajes antiguos
bot.skip_pending = True

@bot.message_handler(commands=["exec"])
def exec(m):
    command = m.text.split(" ", 1)[1]
    call(command.split(" "))
    bot.send_message(m.chat.id, "*{}* executed".format(m.text.split(" ", 1)[1]), parse_mode="Markdown")

@bot.message_handler(commands=["yt"])
def youtube(m):
    link = m.split(" ", 1)[1]
    # exec
    call(["ytcli", "-o", "hdmi", link])
    bot.send_message(m.chat.id, "Reproducing video!")

print("Running...")
bot.polling()
