from telegram.ext import Updater, CommandHandler
import telegram
import logging

# Steam Constants
steamAPIKey = '55B92D3F605D8500F4FAC0C8FB21C685'
steamMatchHistoryCall = 'https://api.steampowered.com/IDOTA2MATCH_570/GetMatchHistory/V001/?account_id={}&key=' + steamAPIKey

#OpenDota Constants
openDotaMatchInfoCall = 'https://api.opendota.com/api/players/{}/recentMatches'
# One bot to rule them all
bot = telegram.Bot(token='257069062:AAEuddnPDHuw5KlTLrL5eOiTEs9-xllqV9w')
updater = Updater(token='257069062:AAEuddnPDHuw5KlTLrL5eOiTEs9-xllqV9w')
dispatcher = updater.dispatcher
feeders = {
    "Brent": '3763200887',
    "Chris": '290262710',
    "Elijah": '146700431',
    "Eric": '189426584',
    "Hannah": '246783176',
    "Luis": '27832643',
    "Tucker": '364488795'
    }

feederDeaths = {
    "Brent": 0,
    "Chris": 0,
    "Elijah": 0,
    "Eric": 0,
    "Hannah": 0,
    "Luis": 0,
    "Tucker": 0
    }

feederWorstMatchId = {
    "Brent": 0,
    "Chris": 0,
    "Elijah": 0,
    "Eric": 0,
    "Hannah": 0,
    "Luis": 0,
    "Tucker": 0
}
# logging to diagnose my many issues. If only it worked in real life :v
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# print bot information. Good to know if we have a working bot.
bot.getMe()

# Hello, world!
def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Beep Doot. You have awoken me.")

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

# TIME TO START THE FEED PARSING
def topFeeds(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Public humiliation is key to improvement.\n")

    for feeder in feeders:
        logger.info("Getting information for " + feeder)
        resp = requests.get(openDotaMatchInfoCall.format(feeders[feeder]))

        if resp.status_code != 200:
            logger.error("Error getting player information | ID: " + feeder)
            bot.send_message(chat_id=update.message.chat_id, text="Error getting player information | ID: " + feeder)

        matches = resp.json()
        logger.debug(matches)

        # Add up deaths for the feeder
        for match in matches:
            localDeathMax = 0
            feederDeaths[feeder] += match['deaths']

            if match['deaths'] > localDeathMax:
                localDeathMax = match['deaths']
                feederWorstMatchId = match['match_id']


# start polling.
updater.start_polling()

# dispatcher handlers.
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(MessageHandler(Filters.command, unknown)), group=1)
