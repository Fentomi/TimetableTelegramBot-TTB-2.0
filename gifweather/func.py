#на вход поступает информация от парсера погоды, выдаем лист(нулевой элемент которого должен отправится на фильтр, а первый- на генерацию гиф)
def text_transform(parser_weather_text=str) -> list:
    first_list = parser_weather_text.split('\n')
    go_to_filter = first_list[1]
    go_to_info = first_list[0]
    try:
        go_to_info_list = go_to_info.split(',')[2]
    except:
        print(go_to_info)
    go_to_info = ''.join(go_to_info_list.split(' ', maxsplit=1)).capitalize()

    list_return = [go_to_filter, go_to_info]
    
    return list_return