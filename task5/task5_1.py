from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from datetime import datetime, timedelta
from pymongo import MongoClient


def conv_str_with_date_to_single_format(date_str):
    """"Функция преобразует строку с датой к единому формату"""
    if 'сегодня' in date_str.split(',')[0].lower():
        str_1 = datetime.today().strftime('%d %m %Y,') + date_str.split(',')[1]
    elif 'вчера' in date_str.split(',')[0].lower():
        str_1 = (datetime.today() - timedelta(days=1)).strftime('%d %m %Y,') + date_str.split(',')[1]
    elif len(date_str.split(',')[0].split(' ')) == 2:
        str_1 = int_value_from_ru_month(date_str.replace(',', f' {str(datetime.now().year)},'))
    else:
        str_1 = int_value_from_ru_month(date_str)
    result = datetime.strptime(str_1, "%d %m %Y, %H:%M")
    return result.strftime('%d %m %Y, %H:%M')


def int_value_from_ru_month(date_str):
    RU_MONTH_VALUES = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))
    return date_str


def data_collection_from_mail_ru(u_name, u_password):
    """Функция собирает информацию входящие письма(от кого, дата отправки, тема письма, текст письма полный)
     с сайта mail.ru и сохраняет в список"""
    s = Service('./chromedriver')
    url = 'https://account.mail.ru/login/'
    options = Options()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    elem = driver.find_element(By.NAME, 'username')
    elem.send_keys(u_name)
    enter = driver.find_element(By.XPATH, "//div[@class='submit-button-wrap']/button")
    enter.click()
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys(u_password)
    enter = driver.find_element(By.XPATH, "//div[@class='submit-button-wrap']//button")
    enter.click()
    links = []
    el_last = ''
    #for _ in range(4):
    while True:
        elements = driver.find_elements(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a")
        if el_last == elements[-1]:
            break
        for i in elements:
            link = i.get_attribute('href')
            if link not in links:
                links.append(link)
        el_last = elements[-1]
        actions = ActionChains(driver)
        actions.move_to_element(elements[-1])
        actions.perform()
        time.sleep(2)
    letters_info = list()
    for link in links:
        item_info = dict()
        driver.get(link)
        topic = driver.find_element(By.CLASS_NAME, 'thread-subject').text
        date_time = driver.find_element(By.CLASS_NAME, 'letter__date').text
        letter_contact = driver.find_element(By.CLASS_NAME, 'letter-contact')
        text_mail = driver.find_element(By.CLASS_NAME, 'letter-body').text
        item_info['topic'] = topic
        item_info['date_time'] = conv_str_with_date_to_single_format(date_time)
        item_info['letter_contact'] = letter_contact.get_attribute('title')
        item_info['text_mail'] = text_mail
        letters_info.append(item_info)
    return letters_info


def add_inform_to_db(lisp_in, db_n):
    """Функция записывает собранные данные о письмах из списка в БД"""
    for item in lisp_in:
        if db_n.count_documents({'date_time': item['date_time']}) == 0 and db_n.count_documents({'text_mail': item['text_mail']}) == 0:
            db_n.insert_one(item)


def main():
    client = MongoClient('127.0.0.1', 27017)
    db = client['mail_db']
    letters = db.letters
    user_name = 'study.ai_172@mail.ru'
    password = 'NextPassword172#'
    add_inform_to_db(data_collection_from_mail_ru(user_name, password), letters)
    for doc in letters.find({}):
        pprint(doc)


if __name__ == "__main__":
    main()