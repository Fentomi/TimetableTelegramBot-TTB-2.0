from parsers.func import html_get, repair_dayofweek, timetable_text_generator, save_file, dayweek_today
from bs4 import BeautifulSoup
import lxml

def parser_yesterday(url, header) -> str:
    html = html_get(url, header)
    soup = BeautifulSoup(html, 'lxml')
    #если день недели суббота или воскресение
    if dayweek_today == 'Saturday': #если суббота, возвращает сообщение "на завтра расписания нет."
        return 'нет расписания на воскресение.'
    elif dayweek_today == 'Sunday': #если воскресение, то пытается взять следующую неделю и спарсить понедельник.
        container = soup.find('div', class_='row tab-pane active')
        next_container = container.find_next_sibling('div', class_='row tab-pane')
        col = next_container.find('div', class_='list col-md-2')
        paras = col.find_all('div', class_='timetable_sheet')
    elif dayweek_today == 'Friday': #если пятница, то пытается спарсить расписание на субботу
        container = soup.find('div', class_='row tab-pane active')
        col = container.find('div', class_='list last col-md-2')
        paras = col.find_all('div', class_='timetable_sheet')
        if paras == []:
            return 'нет расписания на субботу.'
    else:
        container = soup.find('div', class_='row tab-pane active')
        col = container.find('div', class_='list col-md-2 today').find_next_sibling('div', class_='list col-md-2')
        paras = col.find_all('div', class_='timetable_sheet')

    dayofweek = col.find('div', class_='dayofweek').get_text()
    dayofweek_repair = repair_dayofweek(dayofweek)
    text = f'{dayofweek_repair}\n\n'

    paras = col.find_all('div', class_='timetable_sheet')
    text = timetable_text_generator(paras=paras, text=text)
    
    save_file(html=html, text='timetable')

    return text

if __name__ == '__main__':
    print(parser_yesterday('https://ruz.narfu.ru/?timetable&group=16555', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}))