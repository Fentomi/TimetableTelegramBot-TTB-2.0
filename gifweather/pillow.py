from PIL import Image, ImageDraw, ImageFont
import os.path
from time import strftime, gmtime, time

path = r'gifweather\frames\light_rain'
dayweek_today = strftime('%A', gmtime(time()))

def get_list_gif(path) -> list: #функция считает количество кадров в frames и формирует list.

    gif_list = os.listdir(path)
    gif_list_len = len(gif_list)

    num_list = []
    for i in range(0, gif_list_len):
        num_list.append(i)

    for img in gif_list:
        num = img.split('.')[0]
        num_list[int(num)] = img
    
    return num_list

#функция редактирует каждый кадр в отдельности и формирует лист для будущей гифки.
def frames_edite(gif_list) -> list:
    open_gif_list = []
    for img in gif_list:
        rectangle_fon = Image.open(r'gifweather\frames\rectangle.png') #загружаем фон.
        new_img = Image.open(path+'\\'+img)
        rectangle_fon.paste(new_img,(0,0)) #копируем на фон готовую гифку.
    
        #пишем на гифке нужную нам информацию.
        idraw = ImageDraw.Draw(rectangle_fon) 
        headline = ImageFont.truetype('arial.ttf', size=20)
        text = 'Привет!'
        idraw.text((10,200), text, font=headline)

        open_gif_list.append(rectangle_fon)

    return open_gif_list

# тело программы.
# получает данные с парсера weather_parser
def create_gif(): #создает гиф-изображение для телеграм-бота

    gif_list = get_list_gif(path)
    gif_edited_list = frames_edite(gif_list)

    #сохраняем сгенерированные кадры в гиф-изображение
    gif_edited_list[0].save(
        f'gifweather\gif_ready\{dayweek_today}.gif', 
        save_all=True, 
        append_images=gif_edited_list[1:],
        optimize = True, 
        duration=50, 
        loop=0)

if __name__ == '__main__':
    create_gif()