import requests
from bs4 import BeautifulSoup
import lxml

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}

def parser_weather():
    res = requests.get(r'https://www.gismeteo.ru/weather-severodvinsk-3914/', headers=header)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        weather = res.text
    else:
        with open(r'cache\weather.html') as file:
            print('загрузил сохраненную версию.')
            weather = file.read

    soup = BeautifulSoup(weather, 'lxml')

    container = soup.find('a', class_='weathertab weathertab-block tooltip')
    
    date = container.find('div', class_='date').get_text()
    temp = container.find_all('span', class_='unit unit_temperature_c')
    temp_min = temp[0].get_text()
    temp_max = temp[1].get_text()
    info = container.get('data-text')

    text = f'''Сегодня {date}, температура от {temp_min} до {temp_max}.
{info}.'''

    with open(r'cache\weather.html', 'w', encoding='utf-8') as file:
        file.write(weather)

    return text

if __name__ == '__main__':
    parser_weather()
