import pytest
import ftplib
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@pytest.fixture()
def make_is_target_file():
    from helper import make_is_target_file
    return make_is_target_file


@pytest.fixture()
def get_uid():
    from helper import get_uid
    return get_uid


@pytest.fixture
def config_data():
    from config import get_config_data
    return get_config_data()


@pytest.fixture()
def input_values():
    input_values = {
        'min_uid': 0,
        'max_uid': 0,
        'min_date': 0,
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


@pytest.fixture()
def is_target_file(config_data, make_is_target_file, input_values):
    option = {
        "folder_name": config_data['ftp_folder'],
        "uid": {"min": input_values['min_uid'], "max": input_values['max_uid']},
        "date": {"min": input_values['min_date'], "max": input_values['max_date']},
        "tab": input_values['tab']
    }
    is_target_file = make_is_target_file(option)
    return is_target_file


@pytest.mark.skip()
def test_ftp_file1(is_target_file):
    test_full_file_name = 'NEW/test.jpg'
    assert not is_target_file(test_full_file_name)


@pytest.mark.skip
def test_ftp_file2(is_target_file):
    test_full_file_name = 'NEW/109692_221226_2_1.jpg'
    assert is_target_file(test_full_file_name)


def test_a(session, config_data, is_target_file, get_uid):
    ftp_files = session.nlst(config_data['ftp_folder'])
    target_files = []
    for full_file_name in ftp_files:
        if is_target_file(full_file_name):
            target_files.append(full_file_name)

    target_uids = list(set(map(get_uid, target_files)))
    print(target_uids)
