from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

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
