from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot
import telebot

import messages
import configtools

def answer(bot: TeleBot, 
           message: Message, text: str, 
           parse_mode=None, reply_markup=None):
    try:
        sended_message = bot.send_message(message.chat.id, text, 
                                          parse_mode=parse_mode, 
                                          reply_markup=reply_markup)

        return sended_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            raise Exception(f"Bot has kicked from group {message.chat.id}.")
        else:
            raise(e)

def send_register_message(bot: TeleBot, message: Message):
    answer(bot, message, messages.ADDED_TO_CHAT % configtools.BOT_ALIAS)