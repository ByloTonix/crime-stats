import telebot
from telebot import types
import requests
import io

token = 'TOKEN'
bot = telebot.TeleBot(token)
website = 'https://crime-stats.streamlit.app'

def process_data(action, year=None):
    if action == 'get_crimes':
        response = requests.post('http://localhost:5000/process_data', json={'action': 'get_crimes'})
        return response.content

    elif action == 'get_dataset_info':
        response = requests.post('http://localhost:5000/process_data', json={'action': 'get_dataset_info'})
        return response.json()['result']

    elif action == 'get_graph' and year:
        if 2003 <= year <= 2020:
            response = requests.post('http://localhost:5000/process_data', json={'action': 'get_graph', 'year': year})
            return response.content
        else:
            return "Enter correct data"

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info_1 = types.KeyboardButton("Total Crimes")
    button_info_2 = types.KeyboardButton("Database Info")
    button_info_3 = types.KeyboardButton("Visit Website")
    markup.add(button_info_1, button_info_2, button_info_3)

    bot.send_message(message.chat.id, "Hello, please choose one option", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Total Crimes":
        img_bytes = process_data('get_crimes')
        with io.BytesIO(img_bytes) as img_bytes_io:
            img_bytes_io.seek(0)
            bot.send_photo(message.chat.id, img_bytes_io, caption="The total number of crimes for all time: 45362199.0")

    elif message.text == "Database Info":
        processed_data = process_data('get_dataset_info')
        bot.send_message(message.chat.id, f"Information about dataset: \n\n{processed_data}")
        
    elif message.text == "Visit Website":
        markup = types.InlineKeyboardMarkup()
        button_with_link = types.InlineKeyboardButton("click", url=website)
        markup.add(button_with_link)
        bot.send_message(message.chat.id, f'Here\'s a link to my [BI Dashboard]({website})', parse_mode='MarkdownV2', reply_markup=markup)
        
    elif len(message.text) == 4 and message.text.isdigit():
        year = int(message.text)
        img_bytes = process_data('get_graph', year)
        if isinstance(img_bytes, bytes):
            with io.BytesIO(img_bytes) as img_bytes_io:
                img_bytes_io.seek(0)
                bot.send_photo(message.chat.id, img_bytes_io, caption=f"Crimes in {year}")
        else:
            bot.send_message(message.chat.id, img_bytes)

    else:
        bot.send_message(message.chat.id, "Enter correct command!")

if __name__ == '__main__':
    bot.polling(none_stop=True)
