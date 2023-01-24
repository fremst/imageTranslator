import os
import pyautogui


def get_config_data():
    _config_data = {
        'login_id': None,
        'login_pwd': None,
        'ftp_ip': None,
        'ftp_port': None,
        'ftp_id': None,
        'ftp_pwd': None,
        'ftp_folder': None,
        'ftp_url': None,
        'wait_scroll': 1,
        'wait_alert': 0.1,
    }
    try:
        with open(os.getcwd() + '/config.dat') as file:
            input_data = file.read().splitlines()
    except FileNotFoundError:
        print('config.dat 파일을 찾을 수 없습니다.')
        pyautogui.alert("config.dat 파일을 찾을 수 없습니다.")
        exit(0)

    for key in _config_data:
        for elem in input_data:
            if elem.startswith(key):
                _config_data[key] = elem.split(key + ":")[1].strip()
    if ~_config_data['ftp_folder'].endswith('/'):
        _config_data['ftp_folder'] = _config_data['ftp_folder'] + '/'
    if ~_config_data['ftp_url'].endswith('/'):
        _config_data['ftp_url'] = _config_data['ftp_url'] + '/'
    _config_data['ftp_url'] = _config_data['ftp_url']  # + _config_data['ftp_folder']
    return _config_data


def get_translator_config_data():
    _translator_config_data = {
        'x_position': None,
        'y_position': None,
        'max_wait_time': None,
        'wait_url': None,
        'wait_loading': None,
        'wait_save': None,
        'delete_temp': None,
    }
    try:
        with open(os.getcwd() + '/translator_config.dat') as file:
            input_data = file.read().splitlines()
    except FileNotFoundError:
        print('translator_config.dat 파일을 찾을 수 없습니다.')
        pyautogui.alert("translator_config.dat 파일을 찾을 수 없습니다.")
        exit(0)
    for key in _translator_config_data:
        for elem in input_data:
            if elem.startswith(key):
                _translator_config_data[key] = elem.split(key + ":")[1].strip()
    return _translator_config_data
