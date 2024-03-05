# В разработке!

import telebot
from telebot import types
from datetime import datetime, timedelta

current_time = datetime.now()

users_data = []
user_solves = []
all_users = []

bot = telebot.TeleBot("TOKEN")



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, " + message.from_user.first_name + "!")


def show_stats(message):
    for user in users_data:
            if user['user_id'] == message.from_user.id:
                bot.send_message(message.chat.id, "Ваша статистика:\n" + "Всего солвов: " + str(len(user['solves'])))
                break

def add_solve(message):
    # Получаем текст входящего сообщения
    text = message.text
    # users_data.append({'user_id': message.from_user.id, 'solves': []})
    try:
        task_name = text.split(' ')[0]
        task_flag = text.split(' ')[1]
        url = text.split(' ')[2]
    except:
        return
        

    for user in users_data:
        all_users.append(user['user_id'])
    
    if message.from_user.id not in all_users:
        users_data.append({'user_id': message.from_user.id,'solves': []})

    for user in users_data:
        if user['user_id'] == message.from_user.id:
            user['solves'].append({'task_name': task_name, 'task_flag': task_flag, 'url': url})
            break


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "!stats":
        show_stats(message)
    else:
        add_solve(message)
    print(users_data)



bot.polling()

