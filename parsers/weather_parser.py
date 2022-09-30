from .func import html_get, save_file, wind_info #не забыть под конец изменить на parsers.func
from bs4 import BeautifulSoup
import lxml

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}
url_weather = r'https://www.gismeteo.ru/weather-severodvinsk-3914/'

def parser_weather(url_weather, header) -> str:
    html = html_get(url=url_weather, header=header)
    soup = BeautifulSoup(html, 'lxml')

    container = soup.find('a', class_='weathertab weathertab-block tooltip')
    
    date = container.find('div', class_='date').get_text()
    temp = container.find_all('span', class_='unit unit_temperature_c')
    temp_min = temp[0].get_text()
    temp_max = temp[1].get_text()
    info = container.get('data-text')

    wind_list = soup.find_all('span', class_='wind-unit unit unit_wind_m_s')
    wind_info_list = wind_info(wind_list) #[0]- среднее значение, [1]- минимальное значение, [2]- максимальное значение.

    precipitation_cont = soup.find('div', class_='widget-row widget-row-precipitation-bars row-with-caption')
    precipitation_list = precipitation_cont.find_all('div', class_='row-item')

    precipitation_sum = 0
    for precipitation_item in precipitation_list:
        precipitation = precipitation_item.find('div', class_='item-unit').get_text()

        if precipitation == 'н/д':
            continue
        if ',' in precipitation: #если из precipitation попадается число 0,6 , то мы преобразуем его в флоат.
            a = precipitation.split(',')
            precipitation = f'{a[0]}.{a[1]}'
        
        precipitation_sum += float(precipitation)

    text = f'''<i>Cкорость ветра от {wind_info_list[1]} до {wind_info_list[2]} м/с.</i>\n<i>Cредняя скорость равна {wind_info_list[0]} м/c.</i>\n<b>Температура от {temp_min} до {temp_max} градусов.</b>\n{info}.\nОсадки, мм = {precipitation_sum}'''

    text_info = text

    save_file(html=html, text='weather')

    return text_info

if __name__ == '__main__':
    print(parser_weather('https://www.gismeteo.ru/weather-severodvinsk-3914/', {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}))
