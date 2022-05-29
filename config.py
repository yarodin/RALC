import configparser
import os


def create(path):
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'hl_award_url', 'https://hamlog.online/srr/russia/info.php?c=')
    config.set('Settings', 'hl_award_id', '0000')
    config.set('Settings', 'hl_verified_url', 'https://hamlog.online/api/lists/user-verified.txt')
    config.set('Settings', 'dxcl_host', 'dxspots.com')
    config.set('Settings', 'dxcl_port', '23')
    config.set('Settings', 'mycallsign', 'R1TEST')
    config.set('Settings', 'dx_filter', 'SET/FILTER DXCTY/PASS UA,UA2,UA9')
    config.set('Settings', 'band_mode_filter', 'SET/FILTER DXBM/REJECT 1,2,6')

    config.set('Settings', 'spotter_AF', 'False')
    config.set('Settings', 'spotter_AS', 'True')
    config.set('Settings', 'spotter_EU', 'True')
    config.set('Settings', 'spotter_UA', 'True')
    config.set('Settings', 'spotter_NA', 'False')
    config.set('Settings', 'spotter_SA', 'False')
    config.set('Settings', 'spotter_OC', 'False')

    config.set('Settings', 'use_CW', 'True')
    config.set('Settings', 'use_PH', 'True')
    config.set('Settings', 'use_DIG', 'True')

    config.set('Settings', 'use_10M', 'True')
    config.set('Settings', 'use_12M', 'True')
    config.set('Settings', 'use_15M', 'True')
    config.set('Settings', 'use_17M', 'True')
    config.set('Settings', 'use_20M', 'True')
    config.set('Settings', 'use_30M', 'True')
    config.set('Settings', 'use_40M', 'True')
    config.set('Settings', 'use_80M', 'True')
    config.set('Settings', 'use_160M', 'True')

    config.set('Settings', 'debug', 'False')

    with open(path, "w") as config_file:
        config.write(config_file)


def write(path, cfg):

    config = configparser.ConfigParser()
    config.add_section('Settings')
    for key, value in cfg.items():
        config.set('Settings', key, str(value))

    with open(path, "w") as config_file:
        config.write(config_file)


def read(path):
    if not os.path.exists(path):
        create(path)

    config = configparser.ConfigParser()
    config.read(path)

    cfg = dict()
    try:
        cfg['hl_award_url'] = config.get('Settings', 'hl_award_url')
        cfg['hl_award_id'] = config.get('Settings', 'hl_award_id')
        cfg['hl_verified_url'] = config.get('Settings', 'hl_verified_url')
        cfg['dxcl_host'] = config.get('Settings', 'dxcl_host')
        cfg['dxcl_port'] = config.get('Settings', 'dxcl_port')
        cfg['mycallsign'] = config.get('Settings', 'mycallsign')
        cfg['dx_filter'] = config.get('Settings', 'dx_filter')
        cfg['band_mode_filter'] = config.get('Settings', 'band_mode_filter')

        cfg['spotter_AF'] = True if config.get('Settings', 'spotter_af') == 'True' else False
        cfg['spotter_AS'] = True if config.get('Settings', 'spotter_as') == 'True' else False
        cfg['spotter_EU'] = True if config.get('Settings', 'spotter_eu') == 'True' else False
        cfg['spotter_UA'] = True if config.get('Settings', 'spotter_ua') == 'True' else False
        cfg['spotter_NA'] = True if config.get('Settings', 'spotter_na') == 'True' else False
        cfg['spotter_SA'] = True if config.get('Settings', 'spotter_sa') == 'True' else False
        cfg['spotter_OC'] = True if config.get('Settings', 'spotter_oc') == 'True' else False

        cfg['use_CW'] = True if config.get('Settings', 'use_cw') == 'True' else False
        cfg['use_PH'] = True if config.get('Settings', 'use_ph') == 'True' else False
        cfg['use_DIG'] = True if config.get('Settings', 'use_dig') == 'True' else False

        cfg['use_10M'] = True if config.get('Settings', 'use_10m') == 'True' else False
        cfg['use_12M'] = True if config.get('Settings', 'use_12m') == 'True' else False
        cfg['use_15M'] = True if config.get('Settings', 'use_15m') == 'True' else False
        cfg['use_17M'] = True if config.get('Settings', 'use_17m') == 'True' else False
        cfg['use_20M'] = True if config.get('Settings', 'use_20m') == 'True' else False
        cfg['use_30M'] = True if config.get('Settings', 'use_30m') == 'True' else False
        cfg['use_40M'] = True if config.get('Settings', 'use_40m') == 'True' else False
        cfg['use_80M'] = True if config.get('Settings', 'use_80m') == 'True' else False
        cfg['use_160M'] = True if config.get('Settings', 'use_160m') == 'True' else False

        cfg['debug'] = True if config.get('Settings', 'debug') == 'True' else False

    except configparser.NoOptionError as e:
        raise RuntimeError(e)

    return cfg


if __name__ == '__main__':
    settings = read('settings.ini')
    for key, value in settings.items():
        print(f"{key} : {value}")
