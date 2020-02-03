import configparser
CONFIG_NAME = "Bot settings" 
PATH = "../bot.config"


def readConfig(path, name):
    values = {"telegram_webhook_url": None,
            "bot_alias": None,
            "bot_token": None,
            "bot_port": None,
            "bot_url": None}
    
    config = configparser.ConfigParser()
    config.read(path)
    
    for key in values:
        values[key] = (config.get(name, key))
    
    return values
 
TELEGRAM_WEBHOOK_URL, BOT_ALIAS, BOT_TOKEN, BOT_PORT, BOT_URL = readConfig(PATH, CONFIG_NAME).values()
