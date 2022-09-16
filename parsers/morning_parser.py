import requests
from bs4 import BeautifulSoup

url = 'https://ruz.narfu.ru/?timetable&group=16555'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'}

def parser_morning():
    res = requests.get(url, headers=header)
    res.encoding = 'utf-8'

    if res.status_code == 200:
        html = res.text
    else:
        with open(r'cache\timetable.html') as file:
            html = file.read

    soup = BeautifulSoup(html, 'lxml')

    col = soup.find('div', class_='row tab-pane active').find('div', class_='list col-md-2 today')
    
    dayofweek = col.find('div', class_='dayofweek').get_text()
    dayofweek_split = dayofweek.split(',')
    dayofweek_repair = ''
    for i in dayofweek_split:
        new = ''.join(i.split()) + ' '
        dayofweek_repair += new
    text = f'{dayofweek_repair}\n\n'

    paras = col.find_all('div', class_='timetable_sheet')
    for para in paras:
        num_para = para.find('span', class_='num_para').get_text()
        time_para = 'пустая пара'
        kindOfWork = ''
        discipline = ''
        auditorium = ''
        group = ''

        try:
            time_para = para.find('span', class_='time_para').get_text()
            kindOfWork = para.find('span', class_='kindOfWork').get_text()
            discipline = para.find('span', class_='discipline').get_text()
            auditorium_b = para.find('span', class_='auditorium').find('b').get_text()
            auditorium_other = para.find('span', class_='auditorium').find('b').next_sibling
            group = para.find('span', class_='group').get_text()

            time_para = ''.join(time_para.split())
            auditorium_other = ''.join(auditorium_other.split())

            auditorium_other_split = auditorium_other.split(',')
            auditorium = auditorium_b + ', ' + auditorium_other_split[-1]

        except:
            pass
        if time_para != '' and discipline != '':
            text += f'{num_para}) <u>[{time_para}]</u>\n{kindOfWork}\n<pre>{discipline}</pre>\n{auditorium}\n<i>{group}</i>\n\n'
        else:
            text += f'{num_para}) [{time_para}]\n\n'

    with open(r'cache\timetable.html', 'w', encoding='utf-8') as file:
        file.write(html)

    return text

if __name__ == '__main__':
    parser_morning()