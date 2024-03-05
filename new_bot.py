# В разработке

import telebot
from telebot import types


users_data = []
user_solves = []
all_users = []

bot = telebot.TeleBot("6736013664:AAEKl_kFj9QL55nS1X2iq_SZsuKbdL9tr74")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, " + message.from_user.first_name + "!")




@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Получаем текст входящего сообщения
    text = message.text
    # users_data.append({'user_id': message.from_user.id, 'solves': []})
    try:
        task_name = text.split(' ')[0]
        task_flag = text.split(' ')[1]
        url = text.split(' ')[2]
    except:
        pass
        

    for user in users_data:
        all_users.append(user['user_id'])
    
    if message.from_user.id not in all_users:
        users_data.append({'user_id': message.from_user.id,'solves': []})

    for user in users_data:
        if user['user_id'] == message.from_user.id:
            user['solves'].append({'task_name': task_name, 'task_flag': task_flag, 'url': url})
            break
    

    # response = 'Вы отправили: {}'.format(text)
    # bot.send_message(message.chat.id, response)

    print(users_data)



# Запускаем бота
bot.polling()

