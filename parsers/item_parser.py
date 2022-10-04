from bs4 import BeautifulSoup
import lxml
from parsers.func import html_get, repair_dayofweek, para_text_genetator
from time import strftime, gmtime, time

item_names = [
    'Программирование и основы алгоритмизации',
    'Компьютерная графика',
    'Основы правовых знаний',
    'Прикладная физическая культура и спорт',
    'Математика',
    'Иностранный язык',
    'Информационные технологии',
    'Архитектура вычислительной техники',
    'История',
    'Теория вычислений и алгоритмов'
]

list_dayweeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dict_dayweeks_translate = {
    'понедельник': 'Monday',
    'вторник': 'Tuesday',
    'среда': 'Wednesday',
    'четверг': 'Thursday',
    'пятница': 'Friday',
    'суббота': 'Saturday',
    'воскресение': 'Sunday'
}

def fix_discipline(discipline):
    discipline = discipline.split('(')
    item = discipline[0].strip()
    #print(item)
    return item


def parser_item_thisweek(url, header, item_name) -> str:
    html = html_get(url, header)
    soup = BeautifulSoup(html, 'lxml')

    cont = soup.find('div', class_='row tab-pane active') #this week
    text_final = ''

    #find elements in this week
    cols = cont.find_all('div', class_='col-md-2') #find all colums in this week

    cols_list = list() #сформирую список всей колонок дней недели.
    for col in cols:
        cols_list.append(col)
    dayweek_today = strftime('%A', gmtime(time())) # достаем текущий день недели для того, чтобы высчитать, сколько дней из этой недели нужно парсить
    count_days = 0 
    for col in cols: #здесь я буду вытягивать значения dayofweek и сравнивать с dayofweek_today
        dayofweek = col.find('div', class_='dayofweek').get_text()
        dayofweek_split = dayofweek.split(',')
        dayofweek_repair = ''
        new = ''.join(dayofweek_split[0].split())
        dayofweek_repair += new
        if dict_dayweeks_translate[dayofweek_repair] == dayweek_today:
            count_days += 1
            break
        count_days += 1
    if dayweek_today != 'Sunday':
        position_start = len(cols) - (len(cols) - count_days) - 1 #мы находим номер в списке, с которого надо сделать срез.
        cols_list_new = cols_list[position_start:] #делаем срез расписания.
    else:
        return 'на эту неделю ничего не осталось с:'

    for col in cols_list_new: #for every column
        paras = col.find_all('div', class_='timetable_sheet')
        for para in paras:
            try:
                discipline = para.find('span', class_='discipline').get_text() #try to get item
                discipline = fix_discipline(discipline)
                if item_names[item_names.index(item_name)] == discipline:
                    dayofweek = col.find('div', class_='dayofweek').get_text().strip()
                    dayofweek_repair = f'{dayofweek}\n'
                    text = para_text_genetator(para, dayofweek_repair)
                    text_final += text
            except: #если пустая пара
                pass
    if text_final == '':
        text_final = 'на эту неделю ничего нет с:'
    return text_final

def parser_item_nextweek(url, header, item_name):
    html = html_get(url, header)
    soup = BeautifulSoup(html, 'lxml')
    cont = soup.find('div', class_='row tab-pane active').find_next_sibling() #next week
    text_final = ''

    #find elements in next week
    cols = cont.find_all('div', class_='col-md-2')
    for col in cols: #for every column
        paras = col.find_all('div', class_='timetable_sheet')
        for para in paras:
            try:
                discipline = para.find('span', class_='discipline').get_text() #try to get item
                discipline = fix_discipline(discipline)
                if item_names[item_names.index(item_name)] == discipline:
                    dayofweek = col.find('div', class_='dayofweek').get_text().strip()
                    dayofweek_repair = f'{dayofweek}\n'
                    text = para_text_genetator(para, dayofweek_repair)
                    text_final += text
            except: #если пустая пара
                pass
    if text_final == '':
        text_final = 'на следующую неделю ничего нет с:'
    return text_final
