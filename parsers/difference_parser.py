from bs4 import BeautifulSoup
from parsers.func import timetable_text_generator, save_file
import requests
import lxml

#функция ищет изменения между кэш'ем и текущим сайтом за две недели. если находит изменения, то высылает день, в парах которого произошли изменения.
def parser_difference(url, header):
    text_return = list() #в этот список будем складывать обновления и потом за несколько раз бот их вышлет.

    #загружаем site_html.
    res = requests.get(url=url, headers=header)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        site_html = res.text
    else:
        return 'нет обновления' #обработать.
    
    #загружаем cache_html.
    with open('cache\\timetable.html', encoding='utf-8') as file:
        cache_html = file.read()

    #создаем объекты супа.
    site_soup = BeautifulSoup(site_html, 'lxml')
    cache_soup = BeautifulSoup(cache_html, 'lxml')

    #проверяем через <p class='status'></p>, разнится ли статус у сайта и кэш'а.
    status_site = site_soup.find('p', class_='status').get_text()
    status_cache = cache_soup.find('p', class_='status').get_text()
    if status_site == status_cache:
        return 'нет обновления' #обработать.
    
    #достаем из супа первую неделю(активную)
    cont_first_site = site_soup.find('div', class_='row tab-pane active')
    cont_first_cache = cache_soup.find('div', class_='row tab-pane active')
    if cont_first_site != cont_first_cache: #если есть изменения в первой неделе, то начинаем сравнивать колонки.
        #достаем колонки
        cols_first_site = cont_first_site.find_all('div', class_='col-md-2')
        cols_first_cache = cont_first_cache.find_all('div', class_='col-md-2')
        
        for col_site in cols_first_site: #перебираем колонки сайта.
            count = 0
            for col_cache in cols_first_cache: #перебираем колонки кэш'а, будем искать хоть одно соответствие.
                if col_cache == col_site:
                    count += 1
            if count == 0:
                text_return.append(timetable_text_generator(col_site))
    
    #достаем из супа вторую неделю.
    cont_second_site = site_soup.find('div', class_='row tab-pane')
    cont_second_cache = cache_soup.find('div', class_='row tab-pane')
    if cont_second_site != cont_second_cache: #если есть изменения во второй неделе, то начинаем сравнивать колонки.
        #достаем колонки
        cols_second_site = cont_second_site.find_all('div', class_='col-md-2')
        cols_second_cache = cont_second_cache.find_all('div', class_='col-md-2')

        for col_site in cols_second_site: #перебираем колонки сайта.
            count = 0
            for col_cache in cols_second_cache: #перебираем колонки кэш'а, будем искать хоть одно соответствие.
                if col_cache == col_site:
                    count += 1
            if count == 0: #если не найдено ни одного совпадения, то мы достаем текст с сайта и добавляем его в text_return
                text_return.append(timetable_text_generator(col_site))
    
    #если список пуст- отправляем заготовленную фразу. если список имеет изменения, то высылает список.
    if text_return == []:
        return 'нет обновления' #обработать.
    save_file(site_html, 'timetable')
    return text_return
    
if __name__ == '__main__':
    print(parser_difference(r'https://ruz.narfu.ru/?timetable&group=16555', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}))