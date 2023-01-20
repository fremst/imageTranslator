import pytest
import ftplib
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import get_config_data
from main import is_target_file


@pytest.fixture
def config_data():
    return get_config_data()


@pytest.fixture()
def input_values():
    input_values = {
        'min_uid': 124597,
        'max_uid': 0,
        'min_date': 230119,
        'max_date': 0,
        'tab': [1, 1, 1]
    }
    return input_values


@pytest.fixture()
def session(config_data):
    session = ftplib.FTP()
    session.connect(config_data['ftp_ip'], int(config_data['ftp_port']))
    session.login(config_data['ftp_id'], config_data['ftp_pwd'])
    session.encoding = 'utf-8'
    return session


def test_get_files(config_data, input_values, session):
    print(input_values)

    tab = input_values['tab']
    uid = input_values['min_uid']
    while True:
        if input_values['max_uid'] != 0 and uid > input_values['max_uid']:
            break
        uid = str(uid)
        print('[' + uid + '] 상품 작업중')
        ftp_files = session.nlst(config_data['ftp_folder'])
        ftp_file_count = 0
        # for full_file_name in ftp_files:
        #     file_name = full_file_name[len(config_data['ftp_folder'])::]
        #     print(11)
            # if is_target_file(file_name, full_file_name, input_values, uid):
            #     for (ind, tab_chk) in enumerate(tab):
            #         ind = str(ind)
            #         if file_name[len(uid) + len('yymmdd') + 2] == ind and tab_chk:
            #             ftp_file_count += 1
            #             img_url = config_data['ftp_url'] + full_file_name
        assert True
