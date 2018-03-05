from telegram.ext import Updater, CommandHandler
import telegram
import logging

# One bot to rule them all
bot = telegram.Bot(token='257069062:AAEuddnPDHuw5KlTLrL5eOiTEs9-xllqV9w')
updater = Updater(token='257069062:AAEuddnPDHuw5KlTLrL5eOiTEs9-xllqV9w')

# logging to diagnose my many issues. If only it worked in real life :v
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
# print bot information. Good to know if we have a working bot.
logger.info("Bot information: " + bot.getMe())

# Hello, world!
def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Beep Doot. You have awoken me.")

    # start polling.
    updater.start_polling()
    updater.idle()

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
# run hello when somebody types 'hello'
updater.dispatcher.add_handler(CommandHandler('hello', hello))
