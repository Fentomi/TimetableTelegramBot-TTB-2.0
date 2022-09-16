from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

b1 = KeyboardButton('/привет')
b2 = KeyboardButton('/погода')
b3 = KeyboardButton('/помощь')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.insert(b1).insert(b2).insert(b3)

#кнопки на случай команды /расписание
r1 = KeyboardButton('сегодняшнее')
r2 = KeyboardButton('завтрашнее')

tt_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
tt_buttons.insert(r1).insert(r2)

#кнопки на случай команды /активация
a1 = KeyboardButton('рассылка утреннего расписания')
a2 = KeyboardButton('рассылка изменений на неделе')

a_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
a_buttons.add(a1).add(a2)