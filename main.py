import ftplib
import time
from tkinter import *
import pyautogui
import keyboard
import os
import shutil
from config import get_config_data, get_translator_config_data
from helper import make_is_target_file, get_uid

# pyinstaller main.py -F --upx-dir C:\DevStudy\upx401w64\


def set_input_values(input_values, min_uid, max_uid, min_date, max_date, tab1, tab2, tab3):
    input_values['max_uid'] = int(max_uid)
    input_values['min_uid'] = int(min_uid)
    input_values['min_date'] = int(min_date)
    input_values['max_date'] = int(max_date)
    input_values['tab'] = [tab1, tab2, tab3]


def make_temp_dir():
    if not os.path.exists('temp'):
        os.mkdir('temp')


def connect_session():
    session = ftplib.FTP()
    session.connect(config_data['ftp_ip'], int(config_data['ftp_port']))
    session.login(config_data['ftp_id'], config_data['ftp_pwd'])
    session.encoding = 'utf-8'
    return session


def is_target_file(file_name, full_file_name, input_values, uid):
    return full_file_name.startswith(config_data['ftp_folder'] + uid + '_') \
           and (input_values['min_date'] == 0
                or input_values['min_date'] <= int(file_name[len(uid) + 1:len(uid) + 1 + len('yymmdd'):])) \
           and (input_values['max_date'] == 0
                or int(file_name[len(uid) + 1:len(uid) + 1 + len('yymmdd'):]) <= input_values['max_date'])


def get_img_pos(_img_file_name):
    _img_pos = None
    while _img_pos is None:
        _img_pos = pyautogui.locateCenterOnScreen('images/' + _img_file_name)
    return _img_pos


def translate_img(_img_url, _file_name):
    pyautogui.click(960, 0)

    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.write(_img_url)
    time.sleep(float(translator_config_data['wait_url']))
    pyautogui.press('enter')

    time.sleep(float(translator_config_data['wait_loading']))
    print(_file_name, '이미지 로딩 대기중')
    get_img_pos('image_loaded.png')
    print(_file_name, '이미지 로딩 완료')

    pyautogui.click(int(translator_config_data['center_position']), 500, button='right')
    pyautogui.click(get_img_pos('translate_menu.png'))

    print(_file_name, '이미지 번역 대기중')
    get_img_pos('translate_complete.png')
    print(_file_name, '이미지 번역 완료')

    pyautogui.click(960, 500, button='right')
    pyautogui.click(get_img_pos('save_as.png'))

    print(_file_name, '다운로드 창 대기중')
    get_img_pos('save_as_window.png')
    pyautogui.write(_file_name)
    pyautogui.hotkey('alt', 'd')
    pyautogui.write(os.getcwd()+'/temp')
    pyautogui.press('enter')
    pyautogui.hotkey('alt', 's')
    pyautogui.press('y')
    time.sleep(float(translator_config_data['wait_save']))


def get_popup_url(_uid):
    _url = "https://tmg191.cafe24.com/mall/admin/admin_goods_change_image_all.php?goods_uid=" + _uid
    return _url


def upload_imgs(_session, _temp_files):
    for _file_name in _temp_files:
        print(str(_file_name) + " 업로드 진행중")
        with open(os.getcwd() + '\\temp\\' + _file_name, "rb") as f:
            _full_file_name = config_data['ftp_folder'] + _file_name
            _session.delete(_full_file_name)
            _session.storbinary(
                'STOR /' + _full_file_name, f)


def close_job(_wait_window):
    _wait_window.destroy()
    exit(0)


def detect_pause():
    if keyboard.is_pressed('F4'):
        print('일시 정지')
        os.system("pause")


def main_job():

    input_values = {
        "min_uid": int(0),
        "max_uid": int(0),
        "min_date": int(0),
        "max_date": int(0)
    }

    wait_window = Tk()

    wait_window.wm_attributes("-topmost", 1)
    wait_window.title("대기")
    wait_window.geometry("290x161")

    row = 1
    column = 1
    label1 = Label(wait_window, width=10, text="상품번호>=")
    label1.grid(row=row, column=column)
    entry1 = Entry(wait_window, width=20)
    entry1.insert(0, "0")
    column += 1
    entry1.grid(row=row, column=column, columnspan=3)

    row += 1
    column = 1
    label2 = Label(wait_window, width=10, text="상품번호<=")
    label2.grid(row=2, column=column)
    column += 1
    entry2 = Entry(wait_window, width=20)
    entry2.insert(0, "0")
    entry2.grid(row=row, column=column, columnspan=3)

    row += 1
    column = 1
    label3 = Label(wait_window, width=10, text="날짜>=")
    label3.grid(row=row, column=1)
    column += 1
    entry3 = Entry(wait_window, width=20)
    entry3.insert(0, "0")
    entry3.grid(row=row, column=column, columnspan=3)

    row += 1
    column = 1
    label4 = Label(wait_window, width=10, text="날짜<=")
    label4.grid(row=row, column=column)
    column += 1
    entry4 = Entry(wait_window, width=20)
    entry4.insert(0, "0")
    entry4.grid(row=row, column=column, columnspan=3)

    row += 1
    column = 1
    label5 = Label(wait_window, width=10, text="수정 탭")
    label5.grid(row=5, column=column)

    column += 1
    chk1_var = IntVar()
    chk1_var.set(1)
    chk1 = Checkbutton(wait_window, text="대표", variable=chk1_var, width=2)
    chk1.grid(row=row, column=column)

    column += 1
    chk2_var = IntVar()
    chk2_var.set(1)
    chk2 = Checkbutton(wait_window, text="옵션", variable=chk2_var, width=2)
    chk2.grid(row=row, column=column)

    column += 1
    chk3_var = IntVar()
    chk3_var.set(1)
    chk3 = Checkbutton(wait_window, text="상세", variable=chk3_var, width=2)
    chk3.grid(row=row, column=column)
    button1 = Button(wait_window, width=40, text="진행",
                     command=lambda: [
                         set_input_values(input_values,
                                          entry1.get(),
                                          entry2.get(),
                                          entry3.get(),
                                          entry4.get(),
                                          chk1_var.get(),
                                          chk2_var.get(),
                                          chk3_var.get()),
                         wait_window.destroy()
                     ]
                     )

    row += 1
    column = 1
    button1.grid(row=row, column=column, columnspan=4)
    button2 = Button(wait_window, width=40, text="종료", command=lambda: close_job(wait_window))

    row += 1
    column = 1
    button2.grid(row=row, column=column, columnspan=4)

    wait_window.mainloop()

    make_temp_dir()

    success = int(0)
    fail = int(0)

    session = connect_session()

    option = {
        "folder_name": config_data['ftp_folder'],
        "uid": {"min": input_values['min_uid'], "max": input_values['max_uid']},
        "date": {"min": input_values['min_date'], "max": input_values['max_date']},
        "tab": input_values['tab']
    }
    is_target_file = make_is_target_file(option)

    ftp_files = session.nlst(config_data['ftp_folder'])
    session.close()
    target_files = []
    for full_file_name in ftp_files:
        if is_target_file(full_file_name):
            target_files.append(full_file_name)

    target_files = sorted(target_files)

    target_uids = sorted(list(set(map(get_uid, target_files))))
    full_count = len(target_uids)

    for target_uid in target_uids:
        print('[' + target_uid + '] 상품 작업중')
        try:
            for target_full_file_name in target_files:
                file_name = target_full_file_name[len(config_data['ftp_folder'])::]
                if not file_name.startswith(target_uid + '_'):
                    continue
                img_url = config_data['ftp_url'] + target_full_file_name
                detect_pause()
                translate_img(img_url, file_name)
                if os.path.isfile('temp/' + file_name):
                    print(file_name, '이미지 저장 성공!')
                else:
                    raise Exception('temp/' + file_name + ' 이미지 저장 실패')
        except Exception as e:
            print(e)
            print('작업 중 오류 발생')
            fail += 1

        temp_files = os.listdir(os.getcwd() + '/temp')
        session = connect_session()
        upload_imgs(session, temp_files)
        session.close()

        print('[' + target_uid + '] 전체 번역 및 업로드 성공!')
        if translator_config_data['delete_temp'] == 'Y':
            shutil.rmtree(os.getcwd() + '/temp')
            os.mkdir('temp')
        success += 1

    pyautogui.alert(f'{full_count}중 {success+fail}개의 상품 작업 완료! 성공: {success}, 실패: {fail}')
    print(f'{full_count}중 {success+fail}개의 상품 작업 완료! 성공: {success}, 실패: {fail}')


if __name__ == '__main__':
    config_data = get_config_data()
    translator_config_data = get_translator_config_data()
    while True:
        main_job()
