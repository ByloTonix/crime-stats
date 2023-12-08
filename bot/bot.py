import telebot
from telebot import types
import requests
import io

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
website = 'https://crime-stats.streamlit.app'

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info_1 = types.KeyboardButton("Total Crimes Sum")
    button_info_2 = types.KeyboardButton("Database info")
    button_average = types.KeyboardButton("Visit Website")
    markup.add(button_info_1, button_info_2, button_average)

    bot.send_message(message.chat.id, "Hello, please choose one option", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Total Crimes Sum":
        response = requests.post('http://localhost:5000/process_data', json={'action': 'get_crimes'})
        with io.BytesIO(response.content) as img_bytes_io:
            img_bytes_io.seek(0)
            bot.send_photo(message.chat.id, img_bytes_io, caption="The total number of crimes for all time: 45362199.0")


    elif message.text == "Database info":
        response = requests.post('http://localhost:5000/process_data', json={'action': 'get_dataset_info'})
        processed_data = response.json()['result']
        bot.send_message(message.chat.id, f"Database info: \n\n{processed_data}")
    elif message.text == "Visit Website":
        bot.send_message(message.chat.id, f'Here\'s a link to my BI Dashboard: \n{website}')
    elif len(message.text) == 4 and message.text.isdigit():
        year = int(message.text)
        if 2003 <= year <= 2020:
            response = requests.post('http://localhost:5000/process_data', json={'action': 'get_graph', 'year': year})

            with io.BytesIO(response.content) as img_bytes_io:
                img_bytes_io.seek(0)
                bot.send_photo(message.chat.id, img_bytes_io, caption=f"Crimes in {year}")
        else:
            bot.send_message(message.chat.id, "Enter correct date!")
    else:
        bot.send_message(message.chat.id, "Enter correct command!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
