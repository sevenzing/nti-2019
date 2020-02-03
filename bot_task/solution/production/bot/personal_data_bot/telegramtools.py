from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot
import telebot

from . import messages
from . import configtools

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
            raise e

def send_register_message(bot: TeleBot, message: Message):
    answer(bot, message, messages.ADDED_TO_CHAT % configtools.BOT_ALIAS)


def user_in_chat(bot: TeleBot, chat_id, user_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status != 'left' 
    except telebot.apihelper.ApiException as e:
        if 'user not found' in e.args[0]:
            return False
        else:
            raise e
        