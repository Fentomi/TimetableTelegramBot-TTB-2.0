from parsers.func import html_get, timetable_text_generator, save_file, repair_dayofweek
from time import strftime, gmtime, time
from bs4 import BeautifulSoup

def parser_today(url, header) -> str:
    html = html_get(url, header)
    soup = BeautifulSoup(html, 'lxml')
    dayweek_today = strftime('%A', gmtime(time()))
    
    col = soup.find('div', class_='row tab-pane active').find('div', class_='list col-md-2 today')
    if dayweek_today != 'Saturday':
        try:
            dayofweek = col.find('div', class_='dayofweek').get_text()
            paras = col.find_all('div', class_='timetable_sheet')
        except AttributeError:
            return 'нет расписания на сегодня.'
    else:
        col = soup.find('div', class_='row tab-pane active').find('div', class_='list last col-md-2')
        try:
            dayofweek = col.find('div', class_='dayofweek').get_text()
            paras = col.find_all('div', class_='timetable_sheet')
        except AttributeError:
            return 'нет расписания на сегодня.'
    dayofweek = col.find('div', class_='dayofweek').get_text()
    dayofweek_repair = repair_dayofweek(dayofweek)
    text = f'{dayofweek_repair}\n\n'

    paras = col.find_all('div', class_='timetable_sheet')
    text = timetable_text_generator(paras, text)

    save_file(html, 'timetable')

    return text

if __name__ == '__main__':
    print(parser_today('https://ruz.narfu.ru/?timetable&group=16555', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}))