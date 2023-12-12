import io
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

token = 'TOKEN'
bot = Bot(token)
dp = Dispatcher(bot)
website = 'https://crime-stats.streamlit.app'

async def process_data(action, year=None):
    async with aiohttp.ClientSession() as session:
        if action == 'get_crimes':
            async with session.post('http://localhost:5000/process_data', json={'action': 'get_crimes'}) as response:
                return await response.read()

        elif action == 'get_dataset_info':
            async with session.post('http://localhost:5000/process_data', json={'action': 'get_dataset_info'}) as response:
                return (await response.json())['result']

        elif action == 'get_graph' and year:
            if 2003 <= year <= 2020:
                async with session.post('http://localhost:5000/process_data', json={'action': 'get_graph', 'year': year}) as response:
                    return await response.read()
            else:
                return "Enter correct data"

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info_1 = types.KeyboardButton("Total Crimes")
    button_info_2 = types.KeyboardButton("Database Info")
    button_info_3 = types.KeyboardButton("Visit Website")
    markup.add(button_info_1, button_info_2, button_info_3)

    await bot.send_message(message.chat.id, "Hello, please choose one option", reply_markup=markup)

@dp.message_handler()
async def handle_buttons(message: types.Message):
    if message.text == "Total Crimes":
        img_bytes = await process_data('get_crimes')
        with io.BytesIO(img_bytes) as img_bytes_io:
            img_bytes_io.seek(0)
            await bot.send_photo(message.chat.id, img_bytes_io, caption="The total number of crimes for all time: 45362199.0")

    elif message.text == "Database Info":
        processed_data = await process_data('get_dataset_info')
        await bot.send_message(message.chat.id, f"Information about dataset: \n\n{processed_data}")

    elif message.text == "Visit Website":
        markup = types.InlineKeyboardMarkup()
        button_with_link = types.InlineKeyboardButton("click", url=website)
        markup.add(button_with_link)
        await bot.send_message(message.chat.id, f'Here\'s a link to my [BI Dashboard]({website})', parse_mode='MarkdownV2', reply_markup=markup)

    elif len(message.text) == 4 and message.text.isdigit():
        year = int(message.text)
        img_bytes = await process_data('get_graph', year)
        if isinstance(img_bytes, bytes):
            with io.BytesIO(img_bytes) as img_bytes_io:
                img_bytes_io.seek(0)
                await bot.send_photo(message.chat.id, img_bytes_io, caption=f"Crimes in {year}")
        else:
            await bot.send_message(message.chat.id, img_bytes)

    else:
        await bot.send_message(message.chat.id, "Enter correct command!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
