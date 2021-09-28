import re
import telegram
from flask import Flask, request
from credentials import bot_token, URL
import playlist_processing
app = Flask(__name__)

bot = telegram.Bot(token=bot_token)
@app.route('/{}'.format(bot_token), methods=['POST'])
def bot_interaction():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":

        bot_welcome = """ Welcome to Playlist_converter bot, the bot will allow you to convert your spotify playlist to youtube one. To start, send a link to your spotify playlist"
"""

        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=bot_token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'

app.run()
#if __name__ == '__main__':
    #s = bot.setWebhook('{URL}{HOOK}'.format(URL="http://127.0.0.1:5000", HOOK=bot_token))

#    # bot_interaction()
#     updates = bot.get_updates()
#     print(updates[-1])
#     sp_playlist_id = ""
# __init__.spotify_to_youtube(sp_playlist_id)

