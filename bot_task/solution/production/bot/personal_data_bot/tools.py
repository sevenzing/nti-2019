import re
from . import mongotools
from . import BotAssistant
from . import telegramtools
from . import messages
from . import tools
from . import configtools


def in_private_message(message):
    return message.chat.id == message.from_user.id

def bot_was_mentioned(message):
    if message.text is None:
        return False
    return configtools.BOT_ALIAS in message.text


def get_aliases(text):
    return re.findall(r'@\w+', text)


def process_update(db, message, _type):
    """
    Returns a message to send to the user 
    in response to a command or text
    """

    if not mongotools.user_in_database(db, message.from_user.username):
        user = mongotools.create_new_user(db, message.chat.id, mongotools.normalize_alias(message.from_user.username))
        return messages.START_BOT
    else:
        user = mongotools.get_user(db, message.from_user.username)

    state = user['state']
    
    botAssistant = BotAssistant.BotAssistant(state)

    # TODO: in_a_chat instead of True
    text_to_send = botAssistant.action(db, message, _type=_type)
    if state != botAssistant.get_state():
        mongotools.update_user(db, message.from_user.id, state=botAssistant.get_state()) 
    return text_to_send
    

def try_get_real_name(db, bot, message):
    """
    Returns the message to send to the user
    """

    user_from = mongotools.get_user(db, message.from_user.username) 
    
    # IF USER_FROM NOT IN DATABASE
    if user_from is None:
        return messages.ADDED_TO_CHAT % configtools.BOT_ALIAS
    elif user_from['state'] in [0, 1, 2]:
        return messages.ADDED_TO_CHAT % configtools.BOT_ALIAS


    alias = tools.get_aliases(message.text)[0]
    user = mongotools.get_user(db, alias)
    
    # IF USER_TO NOT IN DATABASE
    if user is None:
        return messages.THERE_IS_NO_SUCH_USER % alias
    elif user['state'] in [0, 1, 2]:
        return messages.THERE_IS_NO_SUCH_USER % alias
    
    # IF USER_TO IS IN THIS CHAT
    print(message.chat.id, user['chat_id'])
    if telegramtools.user_in_chat(bot, message.chat.id, user['chat_id']):
        first_name, second_name = user['name'], user['surname']
        return messages.SEND_REAL_NAME % (alias, first_name, second_name)
    
    # IF USER_TO ISN'T IN THIS CHAT
    else:
        return messages.USER_NOT_IN_THIS_CHAT % alias