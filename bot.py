from parsers import parser_morning, parser_today, parser_yesterday, parser_weather
from gifweather import create_gif
from config import *
from keyboards import kb_client, tt_buttons, a_buttons
from gifweather.func import text_transform
from aiogram import Bot, Dispatcher, types, executor
import time
from parsers.difference_parser import parser_difference


bot = Bot(token)
dp = Dispatcher(bot)
dayweek_today = time.strftime('%A', time.gmtime(time.time()))

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

@dp.message_handler(commands=['зменю'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = 'закрываю.'
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['погода'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = parser_weather(url_weather=url_weather, header=header)
    transorm_text = text_transform(text) #неупорядоченные данные из парсера приобретают удобный для отправки и обработки вид.
    create_gif(transorm_text) #в gif_cache создается гиф-изображение "деньнедели.gif", используя фильтр из transform_text[0] и данные из парсера transform_text[1]
    gif = open(f'gifweather\gif_ready\{dayweek_today}.gif', 'rb')
    await bot.send_animation(chat_id, gif)
    gif.close()
    
@dp.message_handler(commands=['помощь'])
async def main(message: types.message):
    chat_id = message.chat.id
    text = '"/меню" для отображения меню;\n"/зменю" для закрытия меню;\n"/привет" для приветствия\n"/погода" для отображения погоды на сегодняшний день в Северодвинске\n"/активация" для активации утреннего рассыла расписания и рассыла изменений в расписании\n"/расписание" для парсинга актуального расписания'
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
            if (time.gmtime(time.time())[3]+3) > 5 and (time.gmtime(time.time())[3]+3) < 7: #если текущее время больше 5 и меньше 7:
                chat_id = message.chat.id
                text = parser_morning(url=url, header=header)
                await bot.send_message(chat_id=chat_id, text=text)
            time.sleep(3600)
    #отслеживание изменений
    @dp.message_handler(text='рассылка изменений на неделе')
    async def difference_timetable(message: types.message):
        status_difference_timetable = True
        while status_difference_timetable:
            text_return = parser_difference(url, header)
            if text_return == 'нет обновления':
                pass
            elif text_return == '':
                pass
            else:
                for text in text_return:
                    await bot.send_message(chat_id=chat_id, text=text)
            time.sleep(3600)


#команды, связанные с расписанием
@dp.message_handler(commands=['расписание'])
async def timetable(message: types.message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text='сегодняшнее/завтрашнее/на всю неделю?', reply_markup=tt_buttons)
    #если пользователь выбрал "сегодняшнее"
    @dp.message_handler(text='сегодняшнее')
    async def today_timetable(message: types.message):
        chat_id = message.chat.id
        text = parser_today(url=url, header=header)
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    #если пользователь выбрал "завтрашнее"
    @dp.message_handler(text='завтрашнее')
    async def yesterday_timetable(message: types.message):
        chat_id = message.chat.id
        text = parser_yesterday(url=url, header=header)
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='html', reply_markup=types.ReplyKeyboardRemove())

executor.start_polling(dp)