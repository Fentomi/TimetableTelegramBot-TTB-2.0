from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#блок с клавиатурой преподавателей
button_first = KeyboardButton('Водовозова Ю.А. | информатика')
button_second = KeyboardButton('Минеева Т.А. | математика')
button_three = KeyboardButton('Честнейшин Н.В. | история')
button_four = KeyboardButton('Истомина С.М./Попова И.С. | английский(B-группа)')
button_five = KeyboardButton('Платоненков С.В. | архитектура вычислительной техники')
button_six = KeyboardButton('Шумихин Н.А./Голионов А.В. | физкультура')
button_seven = KeyboardButton('Мартюшова Е.В. | немецкий')
button_eight = KeyboardButton('Клепиковская Н.В. | английский (С-группа)')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)

greet_kb.row(button_first, button_second, button_three)
greet_kb.row(button_four, button_five, button_six)
greet_kb.row(button_seven, button_eight)

#блок с клавиатурой предметов
itembtn_one = KeyboardButton('Программирование и основы алгоритмизации')
itembtn_two = KeyboardButton('Компьютерная графика')
itembtn_three = KeyboardButton('Основы правовых знаний')
itembtn_four = KeyboardButton('Прикладная физическая культура и спорт')
itembtn_five = KeyboardButton('Математика')
itembtn_six = KeyboardButton('Иностранный язык')
itembtn_seven = KeyboardButton('Информационные технологии')
itembtn_eight = KeyboardButton('Архитектура вычислительной техники')
itembtn_nine = KeyboardButton('История')
itembtn_ten = KeyboardButton('Теория вычислений и алгоритмов')

item_kb = ReplyKeyboardMarkup(resize_keyboard=True)

item_kb.row(itembtn_one, itembtn_two, itembtn_three)
item_kb.row(itembtn_four, itembtn_five, itembtn_six)
item_kb.row(itembtn_seven, itembtn_eight, itembtn_nine)
item_kb.add(itembtn_ten)