from parsers import parser_today, parser_weather, parser_yesterday
from config import *
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(lambda message: message.text == 'помощь')
async def help(message: types.message):
    await bot.send_message(chat_id=message.chat.id, text='"погода"|"сегодня"|"завтра"')

@dp.message_handler(lambda message: message.text == 'погода')
async def main(message: types.message):
    chat_id = message.chat.id
    text_info = parser_weather(url_weather, header)
    await bot.send_message(chat_id=chat_id, text=text_info, parse_mode='html')
    
@dp.message_handler(lambda message: message.text == 'помощь')
async def main(message: types.message):
    chat_id = message.chat.id
    text = '"привет" для приветствия\n"погода" для отображения погоды на сегодняшний день в Северодвинске'
    await bot.send_message(chat_id=chat_id, text=text)

@dp.message_handler(lambda message: message.text == 'сегодня')
async def today_timetable(message: types.message):
    chat_id = message.chat.id
    text = parser_today(url, header)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='html')

@dp.message_handler(lambda message: message.text == 'завтра')
async def yesterday_timetable(message: types.message):
    chat_id = message.chat.id
    text = parser_yesterday(url, header)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='html')

executor.start_polling(dp)