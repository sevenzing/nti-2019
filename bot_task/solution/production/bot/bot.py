import os
from flask import Flask, request
import telebot

import messages
import telegramtools
from configtools import TELEGRAM_WEBHOOK_URL, BOT_ALIAS, BOT_TOKEN, BOT_PORT, BOT_URL
import tools
import mongotools

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
    

@bot.message_handler(regexp=r'real\s+name\s+of\s+@\w+', func=lambda message: len(message.text.split())==4)
def get_real_name(message):
    """
    User sent "real name of @..."
    """

    text_to_send = tools.get_real_name(db, message)
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
                     func=lambda m: m.chat.id == m.from_user.id)
def process_commands(message):
    """
    User sent a command in bot's private message 
    """

    text_to_send = tools.process_update(db, message, _type='command')
    telegramtools.answer(bot, message, text_to_send)


@bot.message_handler(content_types=['text'], 
                     func=lambda m: m.chat.id == m.from_user.id)
def process_text(message):
    """
    User sent text in bot's private message
    """

    text_to_send = tools.process_update(db, message, _type='text')
    telegramtools.answer(bot, message, text_to_send)


@server.route('/', methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '', 200


if __name__ == '__main__':
    bot.remove_webhook()
    # bot.set_webhook(url=BOT_URL)
    # server.run(host="0.0.0.0", port=int(BOT_PORT))
    db = mongotools.get_db()
    bot.polling()
