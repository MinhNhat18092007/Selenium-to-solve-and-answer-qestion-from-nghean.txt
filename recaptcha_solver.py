

# system libraries
import os
import sys
import urllib
import pydub
import speech_recognition as sr
import re
import random
import time
from datetime import datetime
import requests
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

from patch import download_latest_chromedriver, webdriver_folder_name


def delay(waiting_time=5):
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
        print('[INFO] TOR has been activated. Using this option will change your IP address every 60 secs.')
        print(
            '[INFO] Depending on your luck you might still see: Your Computer or Network May Be Sending Automated Queries.')
        tor_process = create_tor_proxy(SOCKS_PORT, CONTROL_PORT)
        PROXIES = {
            "http": f"socks5://127.0.0.1:{SOCKS_PORT}",
            "https": f"socks5://127.0.0.1:{SOCKS_PORT}"
        }
        response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
    else:
        response = requests.get("http://ip-api.com/json/")
    result = json.loads(response.content)
    print('[INFO] IP Address [%s]: %s %s' % (
    datetime.now().strftime("%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))

    # download latest chromedriver, please ensure that your chrome is up to date
    while True:

        # create chrome driver
        chrome_options = webdriver.ChromeOptions()
        path_to_chromedriver = os.path.normpath(
            os.path.join(os.getcwd(), webdriver_folder_name, "chromedriver.exe")
        )
        if activate_tor:
            chrome_options.add_argument(f"--proxy-server=socks5://127.0.0.1:{SOCKS_PORT}")
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(executable_path=path_to_chromedriver, options=chrome_options)
        delay()
        # go to website
        driver.get("https://atgt.nghean.gov.vn/LoginTest.aspx")

        test = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/fieldset/table/tbody/tr[1]/td[2]/input')
        test.send_keys('trandinhnaht')

        password = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/fieldset/table/tbody/tr[2]/td[2]/input')
        password.send_keys('18092007')

        sleep(10)


        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/fieldset/table/tbody/tr[5]/td[1]/input').click()

        driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/table/tbody/tr[2]/td[1]/div[2]/input').click()

        break

    # main program
    # auto locate recaptcha frames


    delay()

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
    delay()
    """frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(recaptcha_control_frame)"""
    # click on checkbox to activate recaptcha
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()

    # switch to recaptcha audio control frame
    delay()
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(recaptcha_challenge_frame)

    # click on audio challenge
    time.sleep(10)
    driver.find_element(By.ID, "recaptcha-audio-button").click()

    # switch to recaptcha audio challenge frame
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(recaptcha_challenge_frame)

    # get the mp3 audio file
    delay()
    src = driver.find_element(By.ID, "audio-source").get_attribute("src")
    src1 = WebDriverWait(driver.find_element(By.ID, "audio-source").get_attribute("src"), 10)
    print(f"[INFO] Audio src: {src}")

    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    # download the mp3 audio file from the source
    urllib.request.urlretrieve(src, path_to_mp3)

    # load downloaded mp3 audio file as .wav
    sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    sound.export(path_to_wav, format="wav")
    sample_audio = sr.AudioFile(path_to_wav)

    # translate audio to text with google voice recognition
    delay()
    r = sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    key = r.recognize_google(audio)
    print(f"[INFO] Recaptcha Passcode: {key}")

    # key in results and submit
    delay()
    driver.find_element(By.ID, "audio-response").send_keys(key.lower())
    driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
    time.sleep(5)
    driver.switch_to.default_content()
    time.sleep(5)
    driver.find_element(By.ID, "recaptcha-demo-submit").click()
    if (tor_process):
        tor_process.kill()


time.sleep(55)
















































