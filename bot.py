import logging
import os
import re

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import playlist_processing

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# define answer to a /start command
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("""   Hi, this bot is for converting your Spotify playlist into a YouTube one. 
    Simply send a spotify playlist link to get started. """)


# define logic behind the reply
def check(message):
    if_playlist_link = re.search("https://open.spotify.com/playlist/", message)
    if if_playlist_link:
        message = re.split("si=", message, 1)
        message = re.sub("https://open.spotify.com/playlist/", "", message[0])
        message = message[:-1]
        try:
            return playlist_processing.spotify_to_youtube(message)
        except:
            return "There was something wrong with your link, please try again"
    else:
        return "There was something wrong with your link, please try again"


# reply with a link or an error message
def answer(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(check(update.message.text))


def main() -> None:
    """Start the bot."""
    updater = Updater(os.environ.get('bot_token'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
