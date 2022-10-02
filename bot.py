from parsers import parser_today, parser_weather, parser_yesterday, parser_pr_thisweek, list_pr
from config import *
from keyboard import greet_kb
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove

from parsers.pr_parser import parser_pr_nextweek, parser_pr_thisweek

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['weather'])
async def main(message: types.message):
    chat_id = message.chat.id
    text_info = parser_weather(url_weather, header)
    await bot.send_message(chat_id=chat_id, text=text_info, parse_mode='html')
    
@dp.message_handler(commands=['today'])
async def today_timetable(message: types.message):
    chat_id = message.chat.id
    text = parser_today(url, header)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='html')

@dp.message_handler(commands=['yesterday'])
async def yesterday_timetable(message: types.message):
    chat_id = message.chat.id
    text = parser_yesterday(url, header)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='html')

@dp.message_handler(commands=['pr'])
async def teacher_timetable(message: types.message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text='пожалуйста, выберите преподавателя, чьи пары хотите проверить в расписании?', reply_markup=greet_kb)
#блок, который обрабатывает получаемый пользователем преподавателя
@dp.message_handler(lambda message: message.text in list_pr) #проверяет, есть ли текст, введенный пользователем, в списке преподавателей, находящийся в pr_parser.
async def handler_pr(message: types.message):
    chat_id = message.chat.id
    text_thisweek = parser_pr_thisweek(url, header, message.text)
    text_nextweek = parser_pr_nextweek(url, header, message.text)
    await bot.send_message(chat_id=chat_id, text=f'эта неделя:\n {text_thisweek}', parse_mode='html', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=chat_id, text=f'следующая неделя:\n {text_nextweek}', parse_mode='html')

executor.start_polling(dp)