import time

token = '5401569358:AAEyaEhSEubXcOkbtG0YrB6QbMi52O-u4jg'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}
url = r'https://ruz.narfu.ru/?timetable&group=16555'
url_weather = r'https://www.gismeteo.ru/weather-severodvinsk-3914/'
now_hours_time = int(time.strftime('%H', time.gmtime(time.time()))) + 3
dayweek_today = time.strftime('%A', time.gmtime(time.time()))