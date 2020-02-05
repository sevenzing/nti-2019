import os
import telebot

from . import messages
from . import telegramtools
from .configtools import BOT_ALIAS, BOT_TOKEN, BOT_URL
from . import tools
from . import mongotools

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(regexp=r'real\s+name\s+of\s+@\w+', func=lambda message: len(message.text.split())==4)
def get_real_name(message):
    """
    User sent "real name of @..."
    """

    text_to_send = tools.try_get_real_name(db, bot, message)
    telegramtools.answer(bot, message, text_to_send)


@bot.message_handler(func=lambda message: not message.new_chat_member is None,
                     content_types = ['new_chat_members'])    
def check_for_adding(message: telebot.types.Message):
    """
    Someone was added to a group
    """

    if message.new_chat_member.username == bot.get_me().username:
        telegramtools.send_register_message(bot, message)
       

@bot.message_handler(content_types=['text'],
                     func=tools.bot_was_mentioned)
def send_register_message(message):
    """
    User sent alias of bot 
    """
    telegramtools.send_register_message(bot, message)
     

@bot.message_handler(commands=['start', 'register', 'remove', 'help'], 
                     func=tools.in_private_message)
def process_commands(message):
    """
    User sent a command in bot's private message 
    """

    text_to_send = tools.process_update(db, message, _type='command')
    telegramtools.answer(bot, message, text_to_send)


@bot.message_handler(content_types=['text'], 
                     func=tools.in_private_message)
def process_text(message):
    """
    User sent text in bot's private message
    """

    text_to_send = tools.process_update(db, message, _type='text')
    telegramtools.answer(bot, message, text_to_send)


print('==========================')
print(f'Hello from @{bot.get_me().username}!')
print('==========================')

bot.delete_webhook()
print('[INFO] >> Removed webhook\n')
db = mongotools.get_db()
print('[INFO] >> Database has been attached\n')

# Uncomment this to switch the bot to the polling
# Comment this to swith the bot to the webhook
print('[INFO] >> Starting polling ...\n')
bot.polling()


bot.set_webhook(url=BOT_URL)