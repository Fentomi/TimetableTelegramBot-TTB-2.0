from cgitb import text
from unicodedata import name
from bs4 import BeautifulSoup
from parsers.func import html_get, para_text_genetator, save_file, repair_dayofweek
import lxml
from time import strftime, gmtime, time

list_pr = [
    'Водовозова Ю.А. | информатика',
    'Минеева Т.А. | математика',
    'Честнейшин Н.В. | история',
    'Истомина С.М./Попова И.С. | английский(B-группа)',
    'Платоненков С.В. | архитектура вычислительной техники',
    'Шумихин Н.А./Голионов А.В. | физкультура',
    'Мартюшова Е.В. | немецкий',
    'Клепиковская Н.В. | английский (С-группа)'
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

def parser_pr_thisweek(url, header, user_choose):

    #после этого блока кода мы получаем список pr_list, в котором есть либо один, либо два преподавателя.
    pr_list1 = ['', '']
    pr = user_choose.split('|')[0].strip() #достаем фамилию и инициалы преподавателя, которые будет искать в расписании.
    if '/' in pr: #если преподавателя два, то формирует список из двух преподавателей.
        pr_list1 = pr.split('/')
        for i in pr_list1: #убрать лишний пробел в конце инициалов.
            i.strip()  
    if pr_list1[0] == '' and pr_list1[1] == '':
        pr_list1.append(pr)

     
    html = html_get(url=url, header=header)
    soup = BeautifulSoup(html, 'lxml')
    text = ''

    cont = soup.find('div', class_='row tab-pane active') #текущая неделя

    cols = cont.find_all('div', class_='col-md-2')

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

        for col in cols_list_new: #перебираем все колонки
            paras = col.find_all('div', class_='timetable_sheet') #находим в колонке все пары
            for para in paras: #для каждой пары в колонке
                try:
                    name_pr = para.find('span', class_='discipline').find('nobr').get_text() #пытаемся достать имя преподавателя
                    for pr in pr_list1:
                        if name_pr == pr:

                            dayofweek = col.find('div', class_='dayofweek').get_text().strip()
                            dayofweek_repair = f'{dayofweek}\n'

                            text += para_text_genetator(para, dayofweek_repair) #достаем подробности пары и добавляем его к общему тексту.
                except: #если пустая пара
                    pass 
    else:
        text = 'на эту неделю ничего не осталось с:'
    if text == '':
        text = 'ничего нет.'
    return text

def parser_pr_nextweek(url, header, user_choose):


    #после этого блока кода мы получаем список pr_list, в котором есть либо один, либо два преподавателя.
    pr_list1 = ['', '']
    pr = user_choose.split('|')[0].strip() #достаем фамилию и инициалы преподавателя, которые будет искать в расписании.
    if '/' in pr: #если преподавателя два, то формирует список из двух преподавателей.
        pr_list1 = pr.split('/')
        for i in pr_list1: #убрать лишний пробел в конце инициалов.
            i.strip()  
    if pr_list1[0] == '' and pr_list1[1] == '':
        pr_list1.append(pr)


    html = html_get(url=url, header=header)
    soup = BeautifulSoup(html, 'lxml')

    text = ''

    cont = soup.find('div', class_='row tab-pane active') #текущая неделя
    cont_next = cont.find_next_sibling() #следующая неделя

    cols = cont_next.find_all('div', class_='col-md-2')

    for col in cols: #перебираем все колонки
        paras = col.find_all('div', class_='timetable_sheet') #находим в колонке все пары
        for para in paras: #для каждой пары в колонке
            try:
                name_pr = para.find('span', class_='discipline').find('nobr').get_text() #пытаемся достать имя преподавателя
                for pr in pr_list1:
                    if name_pr == pr:
                        dayofweek = col.find('div', class_='dayofweek').get_text().strip()
                        dayofweek_repair = f'{dayofweek}\n'
                        text += para_text_genetator(para, dayofweek_repair) #достаем подробности пары и добавляем его к общему тексту.
            except: #если пустая пара
                pass 
    if text == '':
        text = 'ничего нет.'
    return text

if __name__ == '__main__':
    parser_pr_thisweek()