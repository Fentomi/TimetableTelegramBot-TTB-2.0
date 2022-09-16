from parsers.timetable_parser import parser_timetable
from parsers.weather_parser import parser_weather
from parsers.morning_parser import parser_morning
from parsers.yesterday_parser import parser_yesterday
from config import token
from keyboards import kb_client, tt_buttons, a_buttons

from aiogram import Bot, Dispatcher, types, executor
import time

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['привет'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = f'Привет, {message.from_user.full_name}.'
    await bot.send_message(chat_id=chat_id, text=text)

@dp.message_handler(commands=['меню'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = 'высылаю.'
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=kb_client)

@dp.message_handler(commands=['закрыть меню'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = 'закрываю.'
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['погода'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = parser_weather()
    await bot.send_message(chat_id=chat_id, text=text)
    
@dp.message_handler(commands=['помощь'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = '''"/привет" для приветствия;\n"/погода" для прогноза погоды в Северодвинске;'''
    await bot.send_message(chat_id=chat_id, text=text)

@dp.message_handler(commands=[''])
async def groupparser(message: types.message):
    while True:
        chat_id = message.chat.id
        text = ''

        await bot.send_message(chat_id=chat_id, text=text)

#активация 
@dp.message_handler(commands=['активация'])
async def activation(message: types.message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text='активировать рассылку утреннего расписания/рассылку отслеживания изменений?', reply_markup=a_buttons)
    #утреннее расписание
    @dp.message_handler(text='рассылка утреннего расписания')
    async def every_morning_timetable(message: types.message):
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text='успешно.', reply_markup=types.ReplyKeyboardRemove())
        status_morning_timetable = True
        while status_morning_timetable:
            if (time.gmtime(time.time())[3]+3) > 5 and (time.gmtime(time.time())[3]+3) < 8:
                chat_id = message.chat.id
                text = parser_morning()
                await bot.send_message(chat_id=chat_id, text=text)
            time.sleep(7200)
    #отслеживание изменений
    @dp.message_handler(text='рассылка изменений на неделе')
    async def difference_timetable(message: types.message):
        pass


#команды, связанные с расписанием
@dp.message_handler(commands=['расписание'])
async def timetable(message: types.message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text='сегодняшнее/завтрашнее/на всю неделю?', reply_markup=tt_buttons)
    #если пользователь выбрал "сегодняшнее"
    @dp.message_handler(text='сегодняшнее')
    async def today_timetable(message: types.message):
        chat_id = message.chat.id
        text = parser_morning()
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    #если пользователь выбрал "завтрашнее"
    @dp.message_handler(text='завтрашнее')
    async def yesterday_timetable(message: types.message):
        chat_id = message.chat.id
        text = parser_yesterday()
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=types.ReplyKeyboardRemove())



executor.start_polling(dp)