import datetime

import requests
import re
from bs4 import BeautifulSoup

# Prikaz N4 04.03.2019
regions = {'6Y': 'R6Y', '7Y': 'R6Y',
           '8Z': 'R9Z', '9Z': 'R9Z',
           '8W': 'R9W', '9W': 'R9W',
           '0O': 'R0O',
           '6W': 'R6W', '7W': 'R6W',
           '6Q': 'R6Q', '7Q': 'R6Q',
           '6X': 'R6X', '7X': 'R6X',
           '6I': 'R6I', '7I': 'R6I',
           '6E': 'R6E', '7E': 'R6E',
           '1K': 'R1N', '1N': 'R1N',
           '1I': 'R9X', '8X': 'R9X', '9X': 'R9X',
           '6K': 'R7K', '7K': 'R7K',
           '4S': 'R4S',
           '4U': 'R4U',
           '0Q': 'R0Q',
           '6J': 'R6J', '7J': 'R6J',
           '4P': 'R4P', '4Q': 'R4P', '4R': 'R4P',
           '0Y': 'R0Y',
           '4W': 'R4W',
           '0W': 'R0W',
           '6P': 'R6P', '7P': 'R6P',
           '4Y': 'R4Y', '4Z': 'R4Y',
           '8Y': 'R9Y', '9Y': 'R9Y',
           '0U': 'R0U', '0V': 'R0U',
           '0X': 'R0Z', '0Z': 'R0Z',
           '6A': 'R6A', '6B': 'R6A', '6C': 'R6A', '6D': 'R6A', '7A': 'R6A', '7B': 'R6A', '7C': 'R6A', '7D': 'R6A',
           '0A': 'R0A', '0B': 'R0A', '0H': 'R0A',
           '8F': 'R9F', '8G': 'R9F', '9F': 'R9F', '9G': 'R9F',
           '0L': 'R0L', '0M': 'R0L', '0N': 'R0L',
           '6F': 'R6H', '6G': 'R6H', '6H': 'R6H', '6T': 'R6H', '7F': 'R6H', '7G': 'R6H', '7H': 'R6H', '7T': 'R6H',
           '0C': 'R0C',
           '0J': 'R0J',
           '1O': 'R1O',
           '6U': 'R6U', '6V': 'R6U', '7U': 'R6U', '7V': 'R6U',
           '2Z': 'R3Z', '3Z': 'R3Z', '5Z': 'R3Z',
           '2Y': 'R3Y', '3Y': 'R3Y', '5Y': 'R3Y',
           '2V': 'R3V', '3V': 'R3V', '5V': 'R3V',
           '4A': 'R4A', '4B': 'R4A',
           '1Q': 'R1Q', '1R': 'R1Q', '1S': 'R1Q',
           '2O': 'R3Q', '2Q': 'R3Q', '3K': 'R3Q', '3O': 'R3Q', '3Q': 'R3Q', '5K': 'R3Q', '5O': 'R3Q', '5Q': 'R3Q',
           '2U': 'R3U', '3U': 'R3U', '5U': 'R3U',
           '0R': 'R0S', '0S': 'R0S', '0T': 'R0S',
           '2F': 'R2F', '2K': 'R2F',
           '2X': 'R3X', '3X': 'R3X', '5X': 'R3X',
           '8U': 'R9U', '8V': 'R9U', '9U': 'R9U', '9V': 'R9U',
           '4N': 'R4N', '4O': 'R4N',
           '2N': 'R3N', '3N': 'R3N', '5N': 'R3N',
           '8Q': 'R9Q', '8R': 'R9Q', '9Q': 'R9Q', '9R': 'R9Q',
           '2W': 'R3W', '3W': 'R3W', '5W': 'R3W',
           '1C': 'R1C', '1D': 'R1C', '1E': 'R1C',
           '2G': 'R3G', '3G': 'R3G', '5G': 'R3G',
           '0I': 'R0I',
           '2D': 'R3D', '2H': 'R3D', '3D': 'R3D', '3F': 'R3D', '3H': 'R3D', '5D': 'R3D', '5F': 'R3D', '5H': 'R3D',
           '1Y': 'R1Z', '1Z': 'R1Z',
           '2T': 'R3T', '3T': 'R3T', '5T': 'R3T',
           '1T': 'R1T',
           '8O': 'R9O', '8P': 'R9O', '9O': 'R9O', '9P': 'R9O',
           '8M': 'R9M', '8N': 'R9M', '9M': 'R9M', '9N': 'R9M',
           '8S': 'R9S', '8T': 'R9S', '9S': 'R9S', '9T': 'R9S',
           '2E': 'R3E', '3E': 'R3E', '5E': 'R3E',
           '4F': 'R4F', '4G': 'R4F',
           '1W': 'R1W', '1X': 'R1W',
           '6L': 'R6L', '6M': 'R6L', '6N': 'R6L', '7L': 'R6L', '7M': 'R6L', '7N': 'R6L',
           '2S': 'R3S', '3S': 'R3S', '5S': 'R3S',
           '4H': 'R4H', '4I': 'R4H', '4K': 'R4H',
           '4C': 'R4C', '4D': 'R4C',
           '0F': 'R0F',
           '8C': 'R9C', '8D': 'R9C', '9C': 'R9C', '9D': 'R9C',
           '2L': 'R3L', '3L': 'R3L', '5L': 'R3L',
           '2R': 'R3R', '3R': 'R3R', '5R': 'R3R',
           '2I': 'R3I', '3I': 'R3I', '5I': 'R3I',
           '8H': 'R9H', '8I': 'R9H', '9H': 'R9H', '9I': 'R9H',
           '2P': 'R3P', '3P': 'R3P', '5P': 'R3P',
           '8L': 'R9L', '9L': 'R9L',
           '4L': 'R4L', '4M': 'R4L',
           '8A': 'R9A', '8B': 'R9A', '9A': 'R9A', '9B': 'R9A',
           '2M': 'R3M', '3M': 'R3M', '5M': 'R3M',
           '2A': 'R3A', '2B': 'R3A', '2C': 'R3A', '3A': 'R3A', '3B': 'R3A', '3C': 'R3A', '5A': 'R3A', '5B': 'R3A',
           '5C': 'R3A',
           '1A': 'R1A', '1B': 'R1A', '1F': 'R1A', '1L': 'R1A', '1M': 'R1A',
           '6R': 'R7R', '7R': 'R7R',
           '0D': 'R0D',
           '1P': 'R1P',
           '8J': 'R9J', '9J': 'R9J',
           '0K': 'R0K',
           '8K': 'R9K', '9K': 'R9K',
           }

regions_grfc = {
            'Республика Адыгея (Адыгея)': 'R6Y', 'Республика Алтай': 'R9Z', 'Алтайский край': 'R9Y',
            'Амурская область': 'R0J', 'Архангельская область': 'R1O', 'Астраханская область': 'R6U',
            'Республика Башкортостан': 'R9W', 'Белгородская область': 'R3Z', 'Брянская область': 'R3Y',
            'Республика Бурятия': 'R0O', 'Владимирская область': 'R3V', 'Волгоградская область': 'R4A',
            'Вологодская область': 'R1Q', 'Воронежская область': 'R3Q', 'Город Москва': 'R3A',
            'Город Санкт-Петербург': 'R1A', 'Город Севастополь': 'R7R', 'Республика Дагестан': 'R6W',
            'Еврейская автономная область': 'R0D', 'Забайкальский край': 'R0U', 'Ивановская область': 'R3U',
            'Республика Ингушетия': 'R6Q', 'Иркутская область': 'R0S', 'Кабардино-Балкарская Республика': 'R6X',
            'Калининградская область': 'R2F', 'Республика Калмыкия': 'R6I', 'Калужская область': 'R3X',
            'Камчатский край': 'R0Z', 'Карачаево-Черкесская Республика': 'R6E', 'Республика Карелия': 'R1N',
            'Кемеровская область - Кузбасс': 'R9U', 'Кировская область': 'R4N', 'Республика Коми': 'R9X',
            'Костромская область': 'R3N', 'Краснодарский край': 'R6A', 'Красноярский край': 'R0A',
            'Республика Крым': 'R7K', 'Курганская область': 'R9Q', 'Курская область': 'R3W',
            'Ленинградская область': 'R1C', 'Липецкая область': 'R3G', 'Магаданская область': 'R0I',
            'Республика Марий Эл': 'R4S', 'Республика Мордовия': 'R4U', 'Московская область': 'R3D',
            'Мурманская область': 'R1Z', 'Ненецкий автономный округ': 'R1P', 'Нижегородская область': 'R3T',
            'Новгородская область': 'R1T', 'Новосибирская область': 'R9O', 'Омская область': 'R9M',
            'Оренбургская область': 'R9S', 'Орловская область': 'R3E', 'Пензенская область': 'R4F',
            'Пермский край': 'R9F', 'Приморский край': 'R0L', 'Псковская область': 'R1W',
            'Республика Саха (Якутия)': 'R0Q', 'Республика Северная Осетия - Алания': 'R6J', 'Республика Тыва': 'R0Y',
            'Республика Татарстан (Татарстан)': 'R4P', 'Республика Хакасия': 'R0W', 'Ростовская область': 'R6L',
            'Рязанская область': 'R3S', 'Самарская область': 'R4H', 'Саратовская область': 'R4C',
            'Сахалинская область': 'R0F', 'Свердловская область': 'R9C', 'Смоленская область': 'R3L',
            'Ставропольский край': 'R6H', 'Тамбовская область': 'R3R', 'Тверская область': 'R3I',
            'Томская область': 'R9H', 'Тульская область': 'R3P', 'Тюменская область': 'R9L',
            'Удмуртская Республика': 'R4W', 'Ульяновская область': 'R4L', 'Хабаровский край': 'R0C',
            'Ханты-Мансийский автономный округ - Югра': 'R9J', 'Челябинская область': 'R9A',
            'Чеченская Республика': 'R6P', 'Чувашская Республика - Чувашия': 'R4Y', 'Чукотский автономный округ': 'R0K',
            'Ямало-Ненецкий автономный округ': 'R9K', 'Ярославская область': 'R3M'
            }


def getregion(callsign):
    if re.search(r'^(R[A-Z]{0,2}|U[A-I]{1}[A-Z]{0,1}).*', callsign.upper()) is None:
        return 'NotRUS'
    if re.search(r'/\d', callsign.upper()) is not None:
        return '?'
    marker = re.search(r'\d[A-Z]', callsign.upper())
    if marker is None:
        return '?'
    try:
        region = regions[marker.group(0)]
    except KeyError:
        region = '?'
    return region


def getbandmode(frequency, comment):
    band, mode = None, None
    frequency = float(frequency)
    if frequency <= 2000:
        if frequency <= 1838:
            mode = 'CW'
        elif frequency <= 1843:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '160'
    elif frequency <= 3800:
        if frequency <= 3570:
            mode = 'CW'
        elif frequency <= 3600:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '80'
    elif frequency <= 7200:
        if frequency <= 7040:
            mode = 'CW'
        elif frequency <= 7050 \
                or (frequency >= 7071 and frequency <= 7079):
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '40'
    elif frequency <= 10150:
        if frequency <= 10130:
            mode = 'CW'
        else:
            mode = 'DIG'
        band = '30'
    elif frequency <= 14350:
        if frequency <= 14070:
            mode = 'CW'
        elif frequency <= 14100:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '20'
    elif frequency <= 18168:
        if frequency < 18095:
            mode = 'CW'
        elif frequency < 18109:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '17'
    elif frequency <= 21450:
        if frequency <= 21070:
            mode = 'CW'
        elif frequency <= 21110:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '15'
    elif frequency <= 25000:
        if frequency < 24915:
            mode = 'CW'
        elif frequency <= 24929:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '12'
    elif frequency <= 29200:
        if frequency < 28070:
            mode = 'CW'
        elif frequency <= 28190:
            mode = 'DIG'
        else:
            mode = 'PH'
        band = '10'
    else:
        band = None

    if comment[:4] == 'FT8 ' or comment[:4] == 'FT4 ':
        mode = 'DIG'
    elif comment[:3] == 'CW ':
        mode = 'CW'

    if band is None:
        return '?'
    else:
        return band + "-" + mode


def get_grfc_info(callsign):
    region = '?'
    expire = ''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    try:
        response = requests.get('https://grfc.ru/local/ajax/get_signal.php?type=AMATEUR&signal='+callsign,
                                headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
    except (requests.exceptions.RequestException, Exception) as e:
        raise RuntimeError(e)
    for line in soup.text.split('\n'):
        if line[:7] == 'Регион:':
            try:
                region = regions_grfc[line[8:len(line)]]
            except KeyError:
                region = '?'
        elif line[:17] == 'Срок действия до:':
            expire = datetime.datetime.strptime(line[18:len(line)]+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    return region, expire


if __name__ == '__main__':
    print(get_grfc_info('RP77RZ'))
    print(getbandmode('7023', ' '))
