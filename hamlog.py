import requests
import re
from bs4 import BeautifulSoup


def read(url, id):
    regions = ('R0A', 'R0C', 'R0D', 'R0F', 'R0I', 'R0J', 'R0K', 'R0L', 'R0O', 'R0Q', 'R0S', 'R0U', 'R0W', 'R0Y', 'R0Z',
               'R1A', 'R1C', 'R1N', 'R1O', 'R1P', 'R1Q', 'R1T', 'R1W', 'R1Z',
               'R2F',
               'R3A', 'R3D', 'R3E', 'R3G', 'R3I', 'R3L', 'R3M', 'R3N', 'R3P', 'R3Q', 'R3R', 'R3S', 'R3T', 'R3U', 
               'R3V', 'R3W', 'R3X', 'R3Y', 'R3Z',
               'R4A', 'R4C', 'R4F', 'R4H', 'R4L', 'R4N', 'R4P', 'R4S', 'R4U', 'R4W', 'R4Y',
               'R6A', 'R6E', 'R6H', 'R6I', 'R6J', 'R6L', 'R6P', 'R6Q', 'R6U', 'R6W', 'R6X', 'R6Y',
               'R7K', 'R7R',
               'R9A', 'R9C', 'R9F', 'R9H', 'R9J', 'R9K', 'R9L', 'R9M', 'R9O', 'R9Q', 'R9S', 'R9U', 'R9W', 'R9X', 'R9Y',
               'R9Z',
               '?')
    bandsmodes = ('160-CW', '160-PH', '160-DIG', '80-CW', '80-PH', '80-DIG', '40-CW', '40-PH', '40-DIG',
                  '30-CW', '30-DIG', '20-CW', '20-PH', '20-DIG', '17-CW', '17-PH', '17-DIG', '15-CW', '15-PH', '15-DIG',
                  '12-CW', '12-PH', '12-DIG', '10-CW', '10-PH', '10-DIG', '?')

    db = dict()
    for region in regions:
        db[region] = dict()
        for bandmode in bandsmodes:
            db[region][bandmode] = False

    try:
        response = requests.get(url+id)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find('table', class_='table table-bordered table-sm table-candenced table-responsive-sm')
    except (requests.exceptions.RequestException, Exception) as e:
        raise RuntimeError(e)

    blockstartm1 = False
    blockstartm2 = False
    region = ''
    bmindex = 0
    for child in quotes.recursiveChildGenerator():
        if child.name:
            if child.text != ' ':
                if blockstartm2:
                    if child.text == "\nДиапазоны/Области" \
                                     "\nCWPHDIGICWPHDIGICWPHDIGICWDIGICWPHDIGICWPHDIGICWPHDIGICWPHDIGICWPHDIGI":
                        blockstartm2 = False
                    else:
                        if child.name == 'td' and child.text.strip() == '':
                            if child.next_element.name == 'i':
                                db[region][bandsmodes[bmindex]] = True
                            bmindex += 1
                        if child.name == 'strong':
                            region = child.text
                            bmindex = 0
                if child.name == 'td' and child.text == 'DIG':
                    blockstartm1 = True
                if blockstartm1 and child.name == 'tr' and child.text == '':
                    blockstartm2 = True
    return db


def getverifiedusers(url):
    russiancalls = ''
    try:
        db = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e)
    for callsign in db.text.split("\n"):
        if re.search(r'^(R[A-Z]{0,2}|U[A-I]{1}[A-Z]{0,1}).*', callsign.upper()) is not None:
            russiancalls += callsign.rstrip(' ')+"\n"
    return russiancalls


if __name__ == '__main__':
    hamlogusers = getverifiedusers('https://hamlog.online/api/lists/user-verified.txt')
    if "R1BET\n" in hamlogusers:
        print("YES")
    try:
        hamlogdb = read('https://hamlog.online/srr/russia/info.php?c=', '2195')
    except RuntimeError as err:
        print(err)
        exit()
    for key, value in hamlogdb.items():
        print(f"{key} : {value}")
