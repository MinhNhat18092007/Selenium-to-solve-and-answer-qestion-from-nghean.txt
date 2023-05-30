from PyQt6 import QtCore, QtGui, QtWidgets
import requests
import os
import sys
import urllib
import pydub
import speech_recognition as sr
import re
import random
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import stem.process
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import Select
from patch import download_latest_chromedriver, webdriver_folder_name
import pytesseract
import PIL.Image
import cv2
from tkinter import filedialog
import urllib.request
from PIL import Image
import easyocr
import random
import string
import json


def generate_fullname():
    with open('ho_ten.json', encoding="utf-8") as f:
        data = json.load(f)

    full_names = data['fullnames']
    birth_days = data['birth_day']
    hometowns = data['hometown']
    fullname_random = random.choice(full_names)
    birth_days = random.choice(birth_days)

    return fullname_random, birth_days, hometowns


def generate_username(length):
    characters = string.ascii_letters + string.digits  # Bao gồm chữ cái và chữ số
    username = ''
    for _ in range(length):
        char = random.choice(characters)
        while char.isdigit() and username == '':
            char = random.choice(characters)
        username += char
    return username


# Sử dụng hàm generate_username để tạo ra một username có độ dài 8 kí tự
def delay(driver, waiting_time=5):
    driver.implicitly_wait(waiting_time)


def create_tor_proxy(socks_port, control_port):
    TOR_PATH = os.path.normpath(os.getcwd() + "\\tor\\tor.exe")
    try:
        tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(socks_port),
                'ControlPort': str(control_port),
                'MaxCircuitDirtiness': '300',
            },
            init_msg_handler=lambda line: print(line) if re.search('Bootstrapped', line) else False,
            tor_cmd=TOR_PATH
        )
        print("[INFO] Tor connection created.")
    except:
        tor_process = None
        print("[INFO] Using existing tor connection.")

    return tor_process


def renew_ip(control_port):
    print("[INFO] Renewing TOR ip address.")
    with Controller.from_port(port=control_port) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        controller.close()
    print("[INFO] IP address has been renewed! Better luck next try~")


if __name__ == "__main__":
    name = generate_username(12)
    full_name, birth_day, hometown = generate_fullname()
    phone_number = "0397498285"
    password = "123456789"
    email = "nhat49465@gmail.com"
    ccd = "040207037906"

    SOCKS_PORT = 41293
    CONTROL_PORT = 41294
    USER_AGENT_LIST = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    activate_tor = False
    tor_process = None
    user_agent = random.choice(USER_AGENT_LIST)
    if activate_tor:
        print('[INFO] TOR đã được kích hoạt. Sử dụng tùy chọn này sẽ thay đổi địa chỉ IP của bạn mỗi 60 giây.')
        print(
            '[INFO] Tùy thuộc vào may mắn của bạn, bạn có thể vẫn thấy: Máy tính hoặc mạng của bạn có thể đang gửi các truy vấn tự động.')
        tor_process = create_tor_proxy(SOCKS_PORT, CONTROL_PORT)
        PROXIES = {
            "http": f"socks5://127.0.0.1:{SOCKS_PORT}",
            "https": f"socks5://127.0.0.1:{SOCKS_PORT}"
        }
        response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
    else:
        response = requests.get("http://ip-api.com/json/")
    result = json.loads(response.content)
    print('[INFO] Địa chỉ IP [%s]: %s %s' % (
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))

    # tải về phiên bản chromedriver mới nhất, vui lòng đảm bảo rằng Chrome của bạn đã được cập nhật
    while True:
        name = generate_username(12)
        full_name, birth_day, hometown = generate_fullname()
        phone_number = "0397498285"
        password = "123456789"
        email = "nhat49465@gmail.com"
        ccd = "040207037906"

        # tạo trình duyệt Chrome
        chrome_options = webdriver.ChromeOptions()
        path_to_chromedriver = os.path.normpath(
            os.path.join(os.getcwd(), webdriver_folder_name, "chromedriver.exe")
        )
        if activate_tor:
            chrome_options.add_argument(f"--proxy-server=socks5://127.0.0.1:{SOCKS_PORT}")
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(executable_path=path_to_chromedriver, options=chrome_options)
        delay(driver)
        # đi đến trang web
        driver.get("https://thitructuyen.nghean.gov.vn/RegisterMembers.aspx")

        name_register = driver.find_element(By.XPATH,
                                            '/html/body/form/div[3]/fieldset/table/tbody/tr[1]/td[2]/input')
        name_register.send_keys(name)

        full_name_register = driver.find_element(By.XPATH,
                                                 '/html/body/form/div[3]/fieldset/table/tbody/tr[2]/td[2]/input')
        full_name_register.send_keys(full_name)

        birth_day_register = driver.find_element(By.XPATH,
                                                 '/html/body/form/div[3]/fieldset/table/tbody/tr[3]/td[2]/input')
        birth_day_register.send_keys(birth_day)

        gender = Select(driver.find_element_by_id('drpGioitinh'))
        gender.select_by_value('Nam')

        home_register = driver.find_element(By.XPATH,
                                            '/html/body/form/div[3]/fieldset/table/tbody/tr[5]/td[2]/input')
        home_register.send_keys(hometown)

        oop = Select(driver.find_element_by_name('ddlNhomdoituong'))
        oop.select_by_value('3')

        join_oop = Select(driver.find_element_by_name('ddlDoituong'))
        join_oop.select_by_value('26')

        unit = Select(driver.find_element_by_name('ddlDonvi'))
        unit.select_by_value('186')

        phone_number_register = driver.find_element(By.XPATH,
                                                    '/html/body/form/div[3]/fieldset/table/tbody/tr[8]/td[2]/input')
        phone_number_register.send_keys(phone_number)

        password_register = driver.find_element(By.XPATH,
                                                '/html/body/form/div[3]/fieldset/table/tbody/tr[9]/td[2]/input')
        password_register.send_keys(password)

        re_password_register = driver.find_element(By.XPATH,
                                                   '/html/body/form/div[3]/fieldset/table/tbody/tr[10]/td[2]/input')
        re_password_register.send_keys(password)

        email_register = driver.find_element(By.XPATH,
                                             '/html/body/form/div[3]/fieldset/table/tbody/tr[11]/td[2]/input')
        email_register.send_keys(email)

        ccd_register = driver.find_element(By.XPATH,
                                           '/html/body/form/div[3]/fieldset/table/tbody/tr[12]/td[2]/input')
        ccd_register.send_keys(ccd)

        src = driver.find_element(By.XPATH,
                                  "/html/body/form/div[3]/fieldset/table/tbody/tr[13]/td[2]/div[1]/img").get_attribute(
            "src")

        print(src)

        urllib.request.urlretrieve(src, "Captcha_image.png")

        reader = easyocr.Reader(['vi', 'en'])
        results = reader.readtext('Captcha_image.png')
        key = ""
        for x in results:
            key1 = x[1].strip()
            key = key1

        captcha_key = key.replace(" ", "")
        print(captcha_key)
        captcha_key_register = driver.find_element(By.XPATH,
                                                   '/html/body/form/div[3]/fieldset/table/tbody/tr[13]/td[2]/div[2]/input')
        captcha_key_register.send_keys(captcha_key)
        time.sleep(random.randint(10, 14))

        submit_register = driver.find_element(By.XPATH,
                                              '/html/body/form/div[3]/fieldset/table/tbody/tr[16]/td/input')
        submit_register.click()

        try:
            # Tìm phần tử có id="lbThongbao"
            span_element = driver.find_element_by_id('lbThongbao')

            # Kiểm tra trạng thái hiển thị của phần tử
            if span_element.is_displayed():
                print('Phần tử span hiển thị trên trang web.')

                recaptcha_key_register = driver.find_element(By.XPATH,
                                                             '/html/body/form/div[3]/fieldset/table/tbody/tr[13]/td[2]/div[2]/input')

                recaptcha_key_register.clear()
                password_register = driver.find_element(By.XPATH,
                                                        '/html/body/form/div[3]/fieldset/table/tbody/tr[9]/td[2]/input')
                password_register.send_keys(password)

                re_password_register = driver.find_element(By.XPATH,
                                                           '/html/body/form/div[3]/fieldset/table/tbody/tr[10]/td[2]/input')
                re_password_register.send_keys(password)
                src = driver.find_element(By.XPATH,
                                          "/html/body/form/div[3]/fieldset/table/tbody/tr[13]/td[2]/div[1]/img").get_attribute(
                    "src")

                urllib.request.urlretrieve(src, "Captcha_image.png")

                reader = easyocr.Reader(['vi', 'en'])
                results = reader.readtext('Captcha_image.png')
                key = ""
                for x in results:
                    key1 = x[1].strip()
                    key = key1

                captcha_key = key.replace(" ", "")
                print(captcha_key)
                captcha_key_register = driver.find_element(By.XPATH,
                                                           '/html/body/form/div[3]/fieldset/table/tbody/tr[13]/td[2]/div[2]/input')
                captcha_key_register.send_keys(captcha_key)
                time.sleep(random.randint(10, 14))

                submit_register = driver.find_element(By.XPATH,
                                                      '/html/body/form/div[3]/fieldset/table/tbody/tr[16]/td/input')
                submit_register.click()

                start = driver.find_element(By.XPATH,
                                            '/html/body/form/div[3]/div[2]/table/tbody/tr[2]/td[1]/div[2]/input')
                start.click()

                # Selection solve#############################################################################
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[1]').click()

                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()
                sleep(1)

                # Chon slove cau 2

                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luw cau 2

                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # chuyencau3
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[2]').click()

                # slove cau3
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau 3
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # chuyencau4
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[3]').click()

                # solvecau4
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau4
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # chuyencau5
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[4]').click()

                # solvecau4
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau4
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # CAu6

                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[5]').click()

                # solvecau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau7
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[6]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau8
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[7]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau9
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[8]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau10
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[9]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau11
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[10]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau12
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[11]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau13
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[12]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                # Cau14
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[13]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()
                sleep(1)

                # Cau15
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[14]').click()

                # solve
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

                # luu cau
                driver.find_element(By.XPATH,
                                    '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

                nopbai = driver.find_element(By.XPATH,
                                             '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[4]/input[1]')
                nopbai.send_keys(5)

                try:
                    delay(driver)

                    frames = driver.find_elements(By.TAG_NAME, 'iframe')
                    recaptcha_control_frame = None
                    recaptcha_challenge_frame = None
                    for index, frame in enumerate(frames):
                        if re.search('reCAPTCHA', frame.get_attribute("title")):
                            recaptcha_control_frame = frame

                        if re.search('hết hạn', frame.get_attribute("title")):
                            recaptcha_challenge_frame = frame
                    if not (recaptcha_control_frame and recaptcha_challenge_frame):
                        print("[ERR] Unable to find recaptcha. Abort solver.")
                        sys.exit()
                    # switch to recaptcha frame
                    delay(driver)
                    """frames = driver.find_elements_by_tag_name("iframe")
                    driver.switch_to.frame(recaptcha_control_frame)"""
                    # click on checkbox to activate recaptcha
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
                        (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()

                    # switch to recaptcha audio control frame
                    delay(driver)
                    driver.switch_to.default_content()
                    frames = driver.find_elements(By.TAG_NAME, "iframe")
                    driver.switch_to.frame(recaptcha_challenge_frame)

                    # click on audio challenge
                    time.sleep(random.randint(10, 14))
                    driver.find_element(By.ID, "recaptcha-audio-button").click()

                    # switch to recaptcha audio challenge frame
                    driver.switch_to.default_content()
                    frames = driver.find_elements(By.TAG_NAME, "iframe")
                    driver.switch_to.frame(recaptcha_challenge_frame)

                    # get the mp3 audio file
                    delay(driver)
                    src = driver.find_element(By.ID, "audio-source").get_attribute("src")
                    src1 = WebDriverWait(driver.find_element(By.ID, "audio-source").get_attribute("src"), 10)
                    # print(f"[INFO] Audio src: {src}")

                    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
                    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

                    # download the mp3 audio file from the source
                    urllib.request.urlretrieve(src, path_to_mp3)
                except:
                    print("[INFO] IP address has been blocked for recaptcha.")
                    if activate_tor:
                        renew_ip(CONTROL_PORT)
                    sys.exit()

                    # load downloaded mp3 audio file as .wav
                sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                sound.export(path_to_wav, format="wav")
                sample_audio = sr.AudioFile(path_to_wav)

                # translate audio to text with google voice recognition
                delay(driver)
                r = sr.Recognizer()
                with sample_audio as source:
                    audio = r.record(source)
                key = r.recognize_google(audio)
                # print(f"[INFO] Recaptcha Passcode: {key}")

                # key in results and submit
                delay(driver)
                driver.find_element(By.ID, "audio-response").send_keys(key.lower())
                driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
                time.sleep(5)
                driver.switch_to.default_content()
                time.sleep(5)
                # driver.find_element(By.ID, "recaptcha-demo-submit").click()
                if (tor_process):
                    tor_process.kill()
                driver.find_element(By.XPATH,
                                    "/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[4]/input[2]").click()
                driver.save_screenshot("screenshotcut.png")

                driver.close()
                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                from email.mime.image import MIMEImage

                # Thông tin đăng nhập vào tài khoản email
                sender_email = 'minhnhat18092007113@gmail.com'
                sender_password = 'nbaplqrklhrtbpqm'

                # Thông tin người nhận email
                receiver_email = 'trandinhnhatngocrongk7@gmail.com'

                # Tạo đối tượng MIMEMultipart
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = receiver_email
                message['Subject'] = 'Chia sẻ ảnh'

                # Đính kèm file ảnh
                image_path = 'D:\\DocumentPy\\ATGTSele\\screenshotcut.png'  # Đường dẫn đến file ảnh trên máy tính của bạn
                with open(image_path, 'rb') as file:
                    image_data = file.read()

                image_mime = MIMEImage(image_data)
                image_mime.add_header('Content-Disposition', 'attachment', filename='image.png')
                message.attach(image_mime)

                # Gửi email
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    print('Email đã được gửi thành công!')
                except Exception as e:
                    print('Đã xảy ra lỗi trong quá trình gửi email:', str(e))


            else:
                print('Phần tử span không hiển thị trên trang web.')
        except:

            start = driver.find_element(By.XPATH,
                                        '/html/body/form/div[3]/div[2]/table/tbody/tr[2]/td[1]/div[2]/input')
            start.click()

            # Selection solve#############################################################################
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[1]').click()

            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()
            sleep(1)

            # Chon slove cau 2

            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luw cau 2

            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # chuyencau3
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[2]').click()

            # slove cau3
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau 3
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # chuyencau4
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[3]').click()

            # solvecau4
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau4
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # chuyencau5
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[4]').click()

            # solvecau4
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau4
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # CAu6

            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[5]').click()

            # solvecau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau7
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[6]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau8
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[7]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau9
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[8]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau10
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[9]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau11
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[10]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau12
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[11]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau13
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[12]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            # Cau14
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[13]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()
            sleep(1)

            # Cau15
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[3]/span/span/input[14]').click()

            # solve
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[3]/input').click()

            # luu cau
            driver.find_element(By.XPATH,
                                '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/table/tbody/tr/td[1]/span[6]/input').click()

            nopbai = driver.find_element(By.XPATH,
                                         '/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[4]/input[1]')
            nopbai.send_keys(5)

            try:
                delay(driver)

                frames = driver.find_elements(By.TAG_NAME, 'iframe')
                recaptcha_control_frame = None
                recaptcha_challenge_frame = None
                for index, frame in enumerate(frames):
                    if re.search('reCAPTCHA', frame.get_attribute("title")):
                        recaptcha_control_frame = frame

                    if re.search('hết hạn', frame.get_attribute("title")):
                        recaptcha_challenge_frame = frame
                if not (recaptcha_control_frame and recaptcha_challenge_frame):
                    print("[ERR] Unable to find recaptcha. Abort solver.")
                    sys.exit()
                # switch to recaptcha frame
                delay(driver)
                """frames = driver.find_elements_by_tag_name("iframe")
                driver.switch_to.frame(recaptcha_control_frame)"""
                # click on checkbox to activate recaptcha
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()

                # switch to recaptcha audio control frame
                delay(driver)
                driver.switch_to.default_content()
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                driver.switch_to.frame(recaptcha_challenge_frame)

                # click on audio challenge
                time.sleep(random.randint(10, 14))
                driver.find_element(By.ID, "recaptcha-audio-button").click()

                # switch to recaptcha audio challenge frame
                driver.switch_to.default_content()
                frames = driver.find_elements(By.TAG_NAME, "iframe")
                driver.switch_to.frame(recaptcha_challenge_frame)

                # get the mp3 audio file
                delay(driver)
                src = driver.find_element(By.ID, "audio-source").get_attribute("src")
                src1 = WebDriverWait(driver.find_element(By.ID, "audio-source").get_attribute("src"), 10)
                # print(f"[INFO] Audio src: {src}")

                path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
                path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, path_to_mp3)
            except:
                print("[INFO] IP address has been blocked for recaptcha.")
                if activate_tor:
                    renew_ip(CONTROL_PORT)
                sys.exit()

                # load downloaded mp3 audio file as .wav
            sound = pydub.AudioSegment.from_mp3(path_to_mp3)
            sound.export(path_to_wav, format="wav")
            sample_audio = sr.AudioFile(path_to_wav)

            # translate audio to text with google voice recognition
            delay(driver)
            r = sr.Recognizer()
            with sample_audio as source:
                audio = r.record(source)
            key = r.recognize_google(audio)
            # print(f"[INFO] Recaptcha Passcode: {key}")

            # key in results and submit
            delay(driver)
            driver.find_element(By.ID, "audio-response").send_keys(key.lower())
            driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
            time.sleep(5)
            driver.switch_to.default_content()
            time.sleep(5)
            # driver.find_element(By.ID, "recaptcha-demo-submit").click()
            if (tor_process):
                tor_process.kill()
            driver.find_element(By.XPATH,
                                "/html/body/form/div[3]/div[2]/table/tbody/tr[1]/td[1]/div[2]/div[4]/input[2]").click()
            driver.save_screenshot("screenshotcut.png")

            driver.close()
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.image import MIMEImage

            # Thông tin đăng nhập vào tài khoản email
            sender_email = 'minhnhat18092007113@gmail.com'
            sender_password = 'nbaplqrklhrtbpqm'

            # Thông tin người nhận email
            receiver_email = 'trandinhnhatngocrongk7@gmail.com'

            # Tạo đối tượng MIMEMultipart
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = 'Chia sẻ ảnh'

            # Đính kèm file ảnh
            image_path = 'D:\\DocumentPy\\ATGTSele\\screenshotcut.png'  # Đường dẫn đến file ảnh trên máy tính của bạn
            with open(image_path, 'rb') as file:
                image_data = file.read()

            image_mime = MIMEImage(image_data)
            image_mime.add_header('Content-Disposition', 'attachment', filename='image.png')
            message.attach(image_mime)

            # Gửi email
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                print('Email đã được gửi thành công!')
            except Exception as e:
                print('Đã xảy ra lỗi trong quá trình gửi email:', str(e))
