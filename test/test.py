import os

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('872411091:AAGPrDtAZcBGwN3imVl8SmOBHuDG0oQDZCs')


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("register", callback_data="cb_yes"),
                               InlineKeyboardButton("asdakskla", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "", show_alert=True, url='https://t.me/fortest1488bot')
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "okey boomer",show_alert=True)

    bot.get_chat_member()

@bot.message_handler(commands=['start'])
def message_handler(message):
    code = message.text[7:]
    #bot.send_message(message.chat.id, "Вы отправили мне строку: " + code)
    if len(code) > 0:
        if bot.get_chat_member(code, message.from_user.id):
            bot.send_message(message.chat.id, f"Вы часть чата {code}")
        else:
            bot.send_message(message.chat.id, f"Вы не часть чата {code}")

    
@bot.message_handler(func=lambda x: True)
def foo(message):
    bot.send_message(message.chat.id, f"https://t.me/fortest1488bot?start={message.chat.id}")


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling()
