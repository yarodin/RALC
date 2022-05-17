import re
from datetime import datetime
import pytz


def decode_char_spot(raw_string):
    # Chop Line from DX-Cluster into pieces and return a dict with the spot data
    # based on https://github.com/dh1tw/pyhamtools
    data = {}

    # Spotter callsign
    array = raw_string[6:15].split('-')
    if len(array) == 0:
        data['spotter'] = raw_string[6:15]
    else:
        data['spotter'] = array[0].replace(':', '').strip()

    if re.search('[\d.]{5,12}', raw_string[10:25]):
        data['frequency'] = float(re.search('[\d.]{5,12}', raw_string[10:25]).group(0))
    else:
        raise ValueError

    data['dx'] = re.sub('[^A-Za-z0-9/]+', '', raw_string[26:38]).strip()
    data['comment'] = re.sub('[^\sA-Za-z0-9.,;#+\-!?$()@/]+', ' ', raw_string[39:69]).strip()
    data['time'] = datetime.now().replace(tzinfo=pytz.UTC)

    return data


if __name__ == '__main__':
    data = decode_char_spot('DX de RN4WA-#:    3522.0  R1996VK      CW 18 dB 28 WPM CQ             1858Z')
    for key, value in data.items():
        print(f"{key} : {value}")
