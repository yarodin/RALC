import os.path
import datetime
import re
import csv
import PySimpleGUI as sg
import threading
import webbrowser

import msgpack
import socket

import config
import haminfo
import hamlog
import spot

# GUI Window Layout
sg.theme('DefaultNoMoreNagging')
font = 'Arial, 11'
table_headers = ['Time', 'Freq', 'DX       ', 'H', 'Comment', '    Spotter']
table_data = []

root = os.path.dirname(__file__)
icon_image = os.path.join(root, 'icons\\radar.ico')

layout_spots = [[sg.Table(table_data, headings=table_headers, display_row_numbers=False,
                          col_widths=[6, 8, 12, 3, 22, 10], justification='c', auto_size_columns=False,
                          alternating_row_color='ghost white', select_mode=sg.TABLE_SELECT_MODE_NONE, num_rows=20,
                          enable_events=True, enable_click_events=True, key='-SPOTTABLE-')],
                [sg.Text('current status:', justification='r', pad=(0, 0), size=56),
                 sg.Text('offline', pad=(0, 0), text_color='red', key='-CURRENT_STATUS-')],
                [sg.Multiline(size=(68, 4), autoscroll=True, reroute_stdout=True,
                              write_only=True, reroute_cprint=True)],
                [sg.Button(button_text='Start', tooltip='Start spot collecting'),
                 sg.Button(button_text='Stop', tooltip='Stop spot collecting'),
                 sg.Button(button_text='Update', tooltip='Force update all data from hamlog'),
                 sg.Button(button_text='Clear', tooltip='Clear spot table'),
                 sg.Button('Exit')]]

layout_settings = [
    [sg.Sizer(1, 5)],
    [sg.Text('Hamlog URL:', size=10), sg.InputText(key='hl_award_url', size=40, tooltip='Russia Award hamlog URL'),
     sg.InputText(key='hl_award_id', size=6, tooltip='4-digit Russia Award user ID')],
    [sg.Text('Hamlog API:', size=10), sg.InputText(key='hl_verified_url', size=48, tooltip='Hamlog users list')],
    [sg.HorizontalSeparator()],
    [sg.Text('CC cluster:', size=10), sg.InputText(key='dxcl_host', size=20, tooltip='Cluster URL'),
     sg.InputText(key='dxcl_port', size=7, tooltip='Cluster port')],
    [sg.Text('Callsign:', size=10), sg.InputText(key='mycallsign', size=10, tooltip='Callsign - cluster login')],
    [sg.HorizontalSeparator()],
    [sg.Text('Spots from:', size=10), sg.Checkbox('AF', key='-S-AF-', size=3, tooltip='Africa'),
     sg.Checkbox('AS', key='-S-AS-', size=3, tooltip='Asia'), sg.Checkbox('EU', key='-S-EU-', size=3, tooltip='Europe'),
     sg.Checkbox('UA', key='-S-UA-', size=3, tooltip='Russia'),
     sg.Checkbox('NA', key='-S-NA-', size=3, tooltip='North America'),
     sg.Checkbox('SA', key='-S-SA-', size=3), sg.Checkbox('OC', key='-S-OC-', size=3, tooltip='South America')],
    [sg.HorizontalSeparator()],
    [sg.Text('Spots mode:', size=10), sg.Checkbox('CW', key='-DX-CW-', size=3),
     sg.Checkbox('PH', key='-DX-PH-', size=3, tooltip='Phone/SSB'),
     sg.Checkbox('DIG', key='-DX-DIG-', size=3, tooltip='FT8/FT4/etc')],
    [sg.HorizontalSeparator()],
    [sg.Text('Spots band:', size=10), sg.Checkbox('10M', key='-DX-10-', size=3),
     sg.Checkbox('12M', key='-DX-12-', size=3), sg.Checkbox('15M', key='-DX-15-', size=3)],
    [sg.Text('', size=10), sg.Checkbox('17M', key='-DX-17-', size=3), sg.Checkbox('20M', key='-DX-20-', size=3),
     sg.Checkbox('30M', key='-DX-30-', size=3)],
    [sg.Text('', size=10), sg.Checkbox('40M', key='-DX-40-', size=3), sg.Checkbox('80M', key='-DX-80-', size=3),
     sg.Checkbox('160M', key='-DX-160-', size=4)],
    [sg.HorizontalSeparator()],
    [sg.Text('Debug', size=10), sg.Checkbox('On', key='-DEBUG-', size=3, tooltip='Show additional debug info')],
    [sg.HorizontalSeparator()],
    [sg.Sizer(1, 123)],
    [sg.Button(button_text='Load', tooltip='Load settings from ini file'),
     sg.Button(button_text='Save', tooltip='Save settings to ini file'),
     sg.Button(button_text='Help', tooltip='Open help')]]
tabgrp = [[sg.TabGroup([[sg.Tab('Spots', layout_spots, key='-SPOTS-'),
                         sg.Tab('Settings', layout_settings, key='-SETTINGS-')]],
                       tab_location='topleft', change_submits=True, key='tabgrp')]]
window = sg.Window('Russia Award Local Cluster v1.0 by R1BET',
                   tabgrp, font=font, icon=icon_image).finalize()

hamlogdb = dict()
ctydb = dict()
hamlogusers = ''


def load_settings():
    loc_cfg = dict()
    try:
        loc_cfg = config.read("settings.ini")
    except RuntimeError as e:
        window.write_event_value(e)
        pause()
        exit()

    window['hl_award_url'].Update(value=loc_cfg['hl_award_url'])
    window['hl_award_id'].Update(value=loc_cfg['hl_award_id'])
    window['hl_verified_url'].Update(value=loc_cfg['hl_verified_url'])
    window['dxcl_host'].Update(value=loc_cfg['dxcl_host'])
    window['dxcl_port'].Update(value=loc_cfg['dxcl_port'])
    window['mycallsign'].Update(value=loc_cfg['mycallsign'])
    window['-DEBUG-'].Update(value=loc_cfg['debug'])

    for spotter in ['AF', 'AS', 'EU', 'UA', 'NA', 'SA', 'OC']:
        if loc_cfg['spotter_' + spotter]:
            window['-S-' + spotter + '-'].Update(True)
        else:
            window['-S-' + spotter + '-'].Update(False)
    for mode in ['CW', 'PH', 'DIG']:
        if loc_cfg['use_' + mode]:
            window['-DX-' + mode + '-'].Update(True)
        else:
            window['-DX-' + mode + '-'].Update(False)
    for band in [10, 12, 15, 17, 20, 30, 40, 80, 160]:
        if loc_cfg['use_' + str(band) + 'M']:
            window['-DX-' + str(band) + '-'].Update(True)
        else:
            window['-DX-' + str(band) + '-'].Update(False)
    return loc_cfg


def save_settings(settings_values):
    cfg['hl_award_url'] = settings_values['hl_award_url']
    cfg['hl_award_id'] = settings_values['hl_award_id']
    cfg['hl_verified_url'] = settings_values['hl_verified_url']
    cfg['dxcl_host'] = settings_values['dxcl_host']
    cfg['dxcl_port'] = settings_values['dxcl_port']
    cfg['mycallsign'] = settings_values['mycallsign']
    cfg['debug'] = settings_values['-DEBUG-']

    for spotter in ['AF', 'AS', 'EU', 'UA', 'NA', 'SA', 'OC']:
        cfg['spotter_' + spotter] = settings_values['-S-' + spotter + '-']
    for mode in ['CW', 'PH', 'DIG']:
        cfg['use_' + mode] = settings_values['-DX-' + mode + '-']
    for band in [10, 12, 15, 17, 20, 30, 40, 80, 160]:
        cfg['use_' + str(band) + 'M'] = settings_values['-DX-' + str(band) + '-']

    config.write('settings.ini', cfg)


def send_cmd(sock, txt):
    txt = txt + '\n'
    sock.send(txt.encode())


def connection(sock, host, port):
    server = (host, int(port))
    connected = False
    while not connected:
        window.write_event_value('-THREAD-', 'Connection...')
        try:
            sock.connect(server)
        except Exception as err:
            window.write_event_value('-THREAD-', 'Impossibile to connect: ' + str(err))
            return False
        else:
            window.write_event_value('-THREAD-', f'Connected to {host}:{port}')
            window.Element('-CURRENT_STATUS-').update('online', text_color='green')
            return True


def pause():
    if os.name == 'nt':
        os.system('pause')
    else:
        os.system('read -p "Press any key to continue"')


def fmodate(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def update_dbs(hl_award_url, hl_award_id, force_upd):
    loc_hamlogdb = dict()
    loc_ctydb = dict()
    loc_hamlogusers = ''
    if not os.path.isfile("hamlog.db") or force_upd \
            or fmodate("hamlog.db").strftime('%Y-%m-%d') != datetime.datetime.today().strftime('%Y-%m-%d'):
        window.write_event_value('-THREAD-', 'Fetching hamlog.db...')
        try:
            loc_hamlogdb = hamlog.read(hl_award_url, hl_award_id)
        except RuntimeError as e:
            window.write_event_value('-THREAD-', e)
        with open("hamlog.db", "wb") as outfile:
            packed = msgpack.packb(loc_hamlogdb)
            outfile.write(packed)
            outfile.close()
    else:
        window.write_event_value('-THREAD-', 'Reading hamlog.db...')
        with open("hamlog.db", "rb") as infile:
            byte_data = infile.read()
        loc_hamlogdb = msgpack.unpackb(byte_data)

    if not os.path.isfile("hlusers.txt") or force_upd \
            or fmodate("hlusers.txt").strftime('%Y-%m-%d') != datetime.datetime.today().strftime('%Y-%m-%d'):
        window.write_event_value('-THREAD-', 'Fetching hlusers.txt...')
        try:
            loc_hamlogusers = hamlog.getverifiedusers(cfg["hl_verified_url"])
        except RuntimeError as e:
            window.write_event_value('-THREAD-', e)
        with open("hlusers.txt", "w") as outfile:
            outfile.write(loc_hamlogusers)
            outfile.close()
    else:
        window.write_event_value('-THREAD-', 'Reading hlusers.txt...')
        with open("hlusers.txt", "r") as infile:
            loc_hamlogusers = infile.read()

    if os.path.isfile("cty.csv"):
        entities = {'AF': list(), 'AS': list(), 'EU': list(), 'NA': list(), 'OC': list(), 'SA': list(), 'UA': list()}
        with open('cty.csv', newline='') as csvfile:
            csvheap = csv.reader(csvfile, delimiter=',', quotechar='|')
            for loc_row in csvheap:
                if loc_row[0][:2] == 'UA' or loc_row[0][:2] == 'R1':
                    entities['UA'].append(row[0].replace('*', ''))
                else:
                    entities[loc_row[3]].append(loc_row[0].replace('*', ''))
            with open("cty.db", "wb") as outfile:
                packed = msgpack.packb(entities)
                outfile.write(packed)
                outfile.close()
            csvfile.close()
            os.remove("cty.csv")

    if os.path.isfile("cty.db"):
        window.write_event_value('-THREAD-', 'Reading cty.db...')
        with open("cty.db", "rb") as infile:
            byte_data = infile.read()
            loc_ctydb = msgpack.unpackb(byte_data)

    return loc_hamlogdb, loc_hamlogusers, loc_ctydb


def cluster_filter_thread(loc_window):
    ses_db = dict()
    t = threading.current_thread()

    hamlogdb, hamlogusers, ctydb = update_dbs(cfg['hl_award_url'], cfg['hl_award_id'], False)

    filters_appiled = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    connection(sock, cfg['dxcl_host'], cfg['dxcl_port'])
    while getattr(t, "do_run", True):
        if getattr(t, "force_upd", False):
            hamlogdb, hamlogusers, ctydb = update_dbs(cfg['hl_award_url'], cfg['hl_award_id'], True)
            t.force_upd = False
        try:
            msg = sock.recv(2048).decode('latin-1')
        except ConnectionResetError:
            window.Element('-CURRENT_STATUS-').update('offline', text_color='red')
            window.write_event_value('-THREAD-ERR-', 'Connection closed by remote host')
            t.do_run = False
            break
        except TimeoutError:
            continue

        for line in msg.splitlines():
            if getattr(t, "force_upd", False):
                hamlogdb, hamlogusers, ctydb = update_dbs(cfg['hl_award_url'], cfg['hl_award_id'], True)
                t.force_upd = False
                break
            if getattr(t, "do_run", False):
                t.do_run = False
                break
            if line.upper().startswith('DX DE ') and filters_appiled:
                # SPOT
                try:
                    spot_data = spot.decode_char_spot(line)
                except ValueError as e:
                    window.write_event_value('-THREAD-ERR-', e)
                    continue
                if re.search(r'R[A-Z]{0,2}\d\d', spot_data['dx']) is None:
                    dx_region = haminfo.getregion(spot_data['dx'])
                    if dx_region == 'NotRUS':
                        continue
                else:
                    if spot_data['dx'] in ses_db:
                        dx_region, ses_expire = ses_db[spot_data['dx']]
                    else:
                        dx_region, ses_expire = haminfo.get_grfc_info(spot_data['dx'])
                        ses_db[spot_data['dx']] = [dx_region, ses_expire]
                dx_bandmode = haminfo.getbandmode(spot_data['frequency'], spot_data['comment'])
                if cfg['debug']:
                    print([spot_data['time'].strftime("%H:%M"), str(spot_data['frequency']) + '  ', spot_data['dx'],
                           spot_data['comment'], spot_data['spotter'] + ' '])
                if hamlogdb[dx_region][dx_bandmode] == '?' or not hamlogdb[dx_region][dx_bandmode]:
                    if hamlogusers.find(spot_data['dx'] + "\n") > -1:
                        is_hamlog_user = '+'
                    else:
                        is_hamlog_user = ''
                    window.write_event_value('-THREAD-spot-', [spot_data['time'].strftime("%H:%M"),
                                                               str(spot_data['frequency']) + '  ', spot_data['dx'],
                                                               is_hamlog_user, spot_data['comment'],
                                                               spot_data['spotter'] + ' '])
            else:
                if 'login:' in line.lower():
                    send_cmd(sock, cfg['mycallsign'])
                    window.write_event_value('-THREAD-', 'Logged')
                if 'Hello ' in line:
                    send_cmd(sock, 'set/nofilter')  # reset all filters
                    if cfg['use_CW']:
                        send_cmd(sock, 'set/skimmer')
                    else:
                        send_cmd(sock, 'set/noskimmer')
                    if cfg['use_DIG']:
                        send_cmd(sock, 'set/ft8')
                        send_cmd(sock, 'set/ft4')
                    else:
                        send_cmd(sock, 'set/noft8')
                        send_cmd(sock, 'set/noft4')
                    send_cmd(sock, cfg['dx_filter'])

                    bands = ['10', '12', '15', '17', '20', '30', '40', '80', '160']
                    all_bands = True
                    for band in bands:
                        if not cfg['use_' + band + 'M']:
                            all_bands = False
                            break
                    if not all_bands or not cfg['use_CW'] or not cfg['use_DIG'] or not cfg['use_PH']:
                        band_filter = ''
                        for band in bands:
                            if not cfg['use_' + band + 'M']:
                                band_filter = band_filter + band + ','
                            else:
                                if not cfg['use_CW']:
                                    band_filter = band_filter + band + '-CW,'
                                if not cfg['use_DIG']:
                                    band_filter = band_filter + band + '-RTTY,'
                                if not cfg['use_PH']:
                                    band_filter = band_filter + band + '-SSB,'
                        send_cmd(sock, cfg['band_mode_filter'] + ',' + band_filter[:-1])
                    else:
                        send_cmd(sock, cfg['band_mode_filter'])

                    spotter_filter = 'SET/FILTER DOC/PASS '
                    entities_list = ['AF', 'AS', 'EU', 'UA', 'NA', 'SA', 'OC']
                    for entity in entities_list:
                        if cfg['spotter_' + entity]:
                            if spotter_filter[-1] != ' ':
                                spotter_filter = spotter_filter + ','
                            spotter_filter = spotter_filter + ','.join(ctydb[entity])
                    send_cmd(sock, spotter_filter)
                    filters_appiled = True
                    loc_window.write_event_value('-THREAD-', 'Filters applied')
    send_cmd(sock, 'BYE')
    sock.close()
    loc_window.write_event_value('-THREAD-', 'Disconnected from ' + cfg['dxcl_host'] + ':' + cfg['dxcl_port'])
    loc_window.Element('-CURRENT_STATUS-').update('offline', text_color='red')


# Settings
cfg = load_settings()

# GUI
cprint = sg.cprint
proc = ''
while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        if proc != '':
            proc.do_run = False
        break
    if event == 'Start':
        proc = threading.Thread(target=cluster_filter_thread, args=(window,),
                                daemon=True, name='Russia Award Local Cluster Proc')
        proc.start()
    elif event == 'Stop':
        if proc != '':
            proc.do_run = False
    elif event == 'Update':
        if proc != '':
            proc.force_upd = True
    elif event == 'Clear':
        table_data.clear()
        window.Element('-SPOTTABLE-').update(values=table_data)
        cprint('Spots cleared')
    elif event == 'Load':
        cfg = load_settings()
    elif event == 'Save':
        save_settings(values)
        sg.Popup('Setting saved.\nRestart cluster to apply!',
                 keep_on_top=True, font=font, icon=icon_image)
    elif event == 'Help':
        webbrowser.open_new(root+'\\help\\index.html')
    elif event == 'tabgrp':
        if values['tabgrp'] == '-SETTINGS-':
            window.Element('Load').set_focus(True)
        elif values['tabgrp'] == '-SPOTS-':
            window.Element('Start').set_focus(True)
    elif event[0] == '-SPOTTABLE-':
        row, column = event[2]
        if row == -1 and column == 3:
            x, y = window.CurrentLocation()
            sg.Popup('H - Hamlog user', auto_close=True, any_key_closes=True, no_titlebar=True,
                     button_type=5, relative_location=(x-930, y-675), non_blocking=True, modal=False, font=font)
    else:
        if '-THREAD-spot-' in values:
            window.Element('-SPOTTABLE-').Widget.column('#2', anchor='e')
            window.Element('-SPOTTABLE-').Widget.column('#3', anchor='w')
            window.Element('-SPOTTABLE-').Widget.column('#5', anchor='w')
            window.Element('-SPOTTABLE-').Widget.column('#6', anchor='e')
            table_data.insert(0, values['-THREAD-spot-'])
            window.Element('-SPOTTABLE-').update(values=table_data)
        if '-THREAD-' in values:
            cprint(values['-THREAD-'])
        if '-THREAD-ERR-' in values:
            cprint(values['-THREAD-ERR-'], text_color='red')
window.close()
