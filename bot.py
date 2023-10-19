# By: k3vg3n

import telebot
from telebot import types
import http.client
import json
from datetime import datetime, timedelta

keyboard_menu = types.InlineKeyboardMarkup()
keyboard_delete_bot_message = types.InlineKeyboardMarkup()
bot = telebot.TeleBot('TOKEN')

current_time = datetime.now()



def get_team_json():
    url = "ctftime.org"
    # Устанавливаем соединение с сервером
    conn = http.client.HTTPSConnection(url)
    # Отправляем GET запрос
    conn.request("GET", "/api/v1/teams/--номер_команды--/")
    # Читаем и декодируем JSON данные
    team_json_data = json.loads(conn.getresponse().read().decode())
    conn.close()

    team_data = {
        "name": team_json_data["name"],
        "country_place": team_json_data["rating"]["2023"]["country_place"],
        "global_rating_place": team_json_data["rating"]["2023"]["rating_place"],
        "rating_points": team_json_data["rating"]["2023"]["rating_points"]
    }
    team_json = json.dumps(team_data)
    return team_json



def get_CTF_json(number):
        url = "ctftime.org"      
        conn = http.client.HTTPSConnection(url)
        conn.request("GET", f"/api/v1/events/{number}/")
        ctf_json_data = json.loads(conn.getresponse().read().decode())
        conn.close()

        currentCTF_data = {
        "name": ctf_json_data["title"],
        "weight": ctf_json_data["weight"],
        "time_start": ctf_json_data["start"],
        "time_end": ctf_json_data["finish"],
        "ctftime_url": ctf_json_data["ctftime_url"],
        "duration_days": ctf_json_data["duration"]["days"],
        "duration_hours": ctf_json_data["duration"]["hours"],
                                                }
        currentCTF = json.dumps(currentCTF_data)
        currentCTF = json.loads(currentCTF)
        return currentCTF
                        


def get_pastCTF():
        pastCTF_list = ["Прошедшие:"]

        with open('C:/Users/event/Desktop/ctf_madoka.txt', 'r') as f:
                for line in f:
                        number = line.strip()
                        currentCTF_data = get_CTF_json(number)

                        name = currentCTF_data['name']
                        weight = currentCTF_data['weight']
                        finish_time = (datetime.fromisoformat(currentCTF_data['time_start']) + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

                        pastCTF_format = f"\n\nCTF: {name}\nВес: {weight}\nОкончился: {finish_time} МСК"

                        if (datetime.fromisoformat(currentCTF_data['time_end']) + timedelta(hours=3)).replace(tzinfo=None) < current_time:
                            pastCTF_list.append(pastCTF_format)
        return pastCTF_list




def get_futureCTF():
        futureCTF_list = ["Будущие:"]

        with open('C:/Users/event/Desktop/ctf_madoka.txt', 'r') as f:
                for line in f:

                        number = line.strip()
                        currentCTF_data = get_CTF_json(number)

                        name = currentCTF_data['name']
                        weight = currentCTF_data['weight']
                        duration_days = currentCTF_data["duration_days"]
                        duration_hours = currentCTF_data["duration_hours"]

                        if duration_days == 0:
                             prefix_days = "0 дней"
                        elif duration_days == 1:
                             prefix_days = f"{duration_days} день"
                        elif duration_days > 1 & duration_days < 5:
                             prefix_days = f"{duration_days} дня"
                        else: 
                             prefix_days = f"{duration_days} дней"

                        if duration_hours == 0:
                             prefix_hours = ""
                        if duration_hours == 1 | duration_hours == 21:
                             prefix_hours = f" и {duration_hours} час"
                        elif (duration_hours > 1 & duration_hours < 5) | (duration_hours > 21 & duration_hours < 25):
                             prefix_hours = f" и {duration_hours} часа"
                        else:
                             prefix_hours = f" и {duration_hours} часов"
                        
                        start_time = (datetime.fromisoformat(currentCTF_data['time_start']) + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

                        futureCTF_format = f"\n\nCTF: {name}\nВес: {weight}\nНачало: {start_time} МСК\nДлительность: {prefix_days}{prefix_hours}"

                        if (datetime.fromisoformat(currentCTF_data['time_start']) + timedelta(hours=3)).replace(tzinfo=None) > current_time:
                            futureCTF_list.append(futureCTF_format)
        return futureCTF_list




        





team_json = get_team_json()
print(team_json)

team_json = json.loads(team_json)
team_name = team_json['name']
team_counry_place = team_json['country_place']
team_global_rating_place = team_json['global_rating_place']
team_rating_points = float(str(team_json['rating_points'])[:-7])



key_past_ctf = types.InlineKeyboardButton(text='Прошедшие CTF', callback_data='past_ctf')
key_future_ctf = types.InlineKeyboardButton(text='Будующие CTF', callback_data='future_ctf')
key_aboutUs = types.InlineKeyboardButton(text='О нас', callback_data='about_us')
key_delete_bot_message = types.InlineKeyboardButton(text='Удалить', callback_data='delete_bot_message')




@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

  if call.data == "past_ctf": 
    msg = f"{' '.join(get_pastCTF())}"
    bot.send_message(call.message.chat.id, msg, reply_markup=keyboard_delete_bot_message)

  if call.data == "future_ctf": 
    msg = f"{' '.join(get_futureCTF())}"
    bot.send_message(call.message.chat.id, msg, reply_markup=keyboard_delete_bot_message) 

  if call.data == "delete_bot_message": 
    bot.delete_message(call.message.chat.id, call.message.message_id)

  if call.data == "about_us":
    
    msg = "Участники: --сокомандники--"
    bot.send_message(call.message.chat.id, msg, reply_markup=keyboard_delete_bot_message, parse_mode='MarkdownV2') 


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  if message.text == "!menu":
      bot.send_message(message.chat.id, text = f"О команде:\n\nИмя: {team_name}\nРейтинг по России: {team_counry_place}\nРейтинг по миру: {team_global_rating_place}\nОчки: {team_rating_points}", reply_markup=keyboard_menu)
  elif message.text == "!help":
      bot.send_message(message.chat.id, "Это справка")





keyboard_menu.add(key_past_ctf, key_future_ctf, key_aboutUs)
keyboard_delete_bot_message.add(key_delete_bot_message)

bot.polling(none_stop=True, interval=0)