from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import matplotlib.pyplot as plt
import requests
import numpy as np
import telegram
import logging

# OpenDota Constants
openDotaMatchInfoCall = 'https://api.opendota.com/api/players/{}/recentMatches'

# One bot to rule them all
bot = telegram.Bot(token='257069062:AAEuddnPDHuw5KlTLrL5eOiTEs9-xllqV9w')
updater = Updater(token='257069062:AAEuddnPDHuw5KlTLrL5eOiTEs9-xllqV9w')
dispatcher = updater.dispatcher

# GLOBAL DICTS
feeders = {
    "Brent": '33167696',
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

feederMaxDeathsInGame = {
    "Brent": 0,
    "Chris": 0,
    "Elijah": 0,
    "Eric": 0,
    "Hannah": 0,
    "Luis": 0,
    "Tucker": 0
}

feederDeathsPerGame = {
"Brent": [],
"Chris": [],
"Elijah": [],
"Eric": [],
"Hannah": [],
"Luis": [],
"Tucker": []
}

# logging to diagnose my many issues. If only it worked in real life :v
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# print bot information. Good to know if we have a working bot.
bot.getMe()


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Beep Doot. You have awoken me.")

def stop(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Beep Doot. Time to go.")

# --------- TIME TO START THE FEED PARSING ----------
def topFeeds(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Public humiliation is key to improvement.\n")

    # Load up feeder information into global dictionaries
    loadFeederInformation()

    # Create output in descending order
    feederString, worstFeeder = calculateWorstFeeder()

    # Display match information for worst feeder and his/her worst game!
    bot.send_message(chat_id=update.message.chat_id, text=feederString)
    congratsMessage = "Congratulations to {}! You are the feeder of the week.".format(worstFeeder)
    if worstFeeder == "Hannah":
        congratsMessage += "\nCheck out the game where she fed the worst ({} times!)".format(feederMaxDeathsInGame[worstFeeder])
    else:
        congratsMessage += "\nCheck out the game where he fed the worst ({} times!)".format(feederMaxDeathsInGame[worstFeeder])

    bot.send_message(chat_id=update.message.chat_id, text=congratsMessage)
    bot.send_message(chat_id=update.message.chat_id, text="https://www.dotabuff.com/matches/{}".format(feederWorstMatchId[worstFeeder]))

    # send chat a graph of feeding
    graphGameInformation(worstFeeder)
    bot.send_photo(chat_id=update.message.chat_id, photo=open('feeds.png', 'rb'))

def loadFeederInformation():
    for feeder in feeders:
        logger.info("Getting information for " + feeder)
        resp = requests.get(openDotaMatchInfoCall.format(feeders[feeder]))

        if resp.status_code != 200:
            logger.error("Error getting player information | ID: " + feeder)
            bot.send_message(chat_id=update.message.chat_id, text="Error getting player information | ID: " + feeder)

        matches = resp.json()
        logger.debug(matches)

        # Clear old data & add up deaths for the feeder
        localDeathMax = 0
        feederDeathsPerGame[feeder] = []
        feederDeaths[feeder] = 0
        for match in matches:

            feederDeaths[feeder] += match['deaths']

            # keep track of deaths per game
            feederDeathsPerGame[feeder].append(match['deaths'])

            # keep track of worst game for feeder
            if match['deaths'] > localDeathMax:
                localDeathMax = match['deaths']
                feederWorstMatchId[feeder] = match['match_id']
                feederMaxDeathsInGame[feeder] = match['deaths']

    logger.debug("Peoples' deaths per game")
    logger.debug(feederMaxDeathsInGame)

def calculateWorstFeeder():
    feederList = sorted(feederDeaths, key=feederDeaths.get, reverse = True)
    logger.info(feederList)

    feederString = "TOP FEEDERS OF THE WEEK (20 matches):\nRank\tName\tDeaths\n"
    feederRank = 1

    for feeder in feederList:
      logger.info(feeder + " " + str(feederDeaths[feeder]))
      feederString += "{}\t{}\t{}".format(str(feederRank), str(feeder), str(feederDeaths[feeder]))
      feederString += "\n"
      feederRank = feederRank+1

    logger.info("FinalString: \n")
    logger.info(feederString)

    return feederString, feederList[0]

def graphGameInformation(worstFeeder):
    # Graph recent game feeding history
    logger.info("Graphing information for worstFeeder" + worstFeeder)
    xAxis=np.arange(len(feederDeathsPerGame[worstFeeder]))
    width=0.8

    # populate the graph
    fig, ax = plt.subplots()
    rects1 = ax.bar(xAxis, feederDeathsPerGame[worstFeeder], width, color='b')

    # label the graph
    ax.set_title("{}'s Graph of Shame".format(worstFeeder))
    ax.set_ylabel("Deaths per Game")
    ax.set_xlabel("Game - Oldest to Newest")

    # save to file
    fig.savefig('feeds.png')

# start polling.
updater.start_polling()

# dispatcher handlers.
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('topFeeds', topFeeds))
