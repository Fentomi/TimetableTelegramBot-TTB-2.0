import time

token = 'enter your token'
header = {'User-Agent': 'enter your User-Agent'}
url = r'https://ruz.narfu.ru/?timetable&group=16555'
url_weather = r'https://www.gismeteo.ru/weather-severodvinsk-3914/'
now_hours_time = int(time.strftime('%H', time.gmtime(time.time()))) + 3
dayweek_today = time.strftime('%A', time.gmtime(time.time()))
