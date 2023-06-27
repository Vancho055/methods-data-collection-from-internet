#Вариант I
#Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
#Логин тестового ящика: study.ai_172@mail.ru
#Пароль тестового ящика: Ferrum123!

#Вариант II
#2) Написать программу, которая собирает товары «Самые просматриваемые» с сайта техники mvideo и
# складывает данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары

from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import os

from selenium.webdriver.support.wait import WebDriverWait

cwd = os.getcwd()

chrome_options = Options()
chrome_options.add_argument('start-maximized')

service = Service(f'{cwd}/chromedriver')
chrome_driver = webdriver.Chrome(service=service, options=chrome_options)


def log_in_mail(driver=chrome_driver):
    driver.get('https://account.mail.ru/login')
    driver.implicitly_wait(10)

    input_login = driver.find_element(By.XPATH, "//input[@name='username']")
    input_login.send_keys("study.ai_172")

    input_login.send_keys(Keys.ENTER)

    input_password = driver.find_element(By.XPATH, "//input[@name='password']")
    input_password.send_keys("NextPassword172#")

    input_password.send_keys(Keys.ENTER)


def load_data_to_mongodb(data, name):
    client = MongoClient(
        f"mongodb+srv://evgeny_varlamov92:27Fifa2010@cluster0"
        f".pnfwt.mongodb.net/{name}?retryWrites=true&w=majority")
    db = client[f'{name}']

    news = db.news
    not_added_data = []
    duplicate_data = []
    for one in data:
        # one['_id'] = f'{one["link"][22:30]}_{one["link_site"][8:10]}'
        try:
            news.insert_one(one)
        except DuplicateKeyError:
            duplicate_data.append(one)
        except:
            not_added_data.append(one)


if __name__ == '__main__':

    log_in_mail(chrome_driver)
    # list_elements = scroll_to_elem()
    inbox_elements = chrome_driver.find_elements(By.XPATH, "//a[contains(@href,'/inbox/0')]")
    # inbox_elements[0].click()
    list_with_message = []
    dict_message = {}
    for i in range(len(inbox_elements)):
        dict_message = {}
        inbox_elements = chrome_driver.find_elements(By.XPATH, "//a[contains(@href,'/inbox/0')]")
        inbox_elements[i].click()
        wait = WebDriverWait(chrome_driver, 30)
        dict_message['!subject'] = chrome_driver.find_element(By.CLASS_NAME, "thread-subject").text
        dict_message['from'] = chrome_driver.find_element(By.CLASS_NAME, "letter-contact").text
        dict_message['date_time'] = chrome_driver.find_element(By.CLASS_NAME, "letter__date").text
        message_elements = chrome_driver.find_elements(By.XPATH,
                                                       "//div[@class='letter-body']//*")
        string_message = ''
        for elem in message_elements:
            string_message += f"{elem.text} "
        dict_message['message'] = string_message
        list_with_message.append(dict_message)
        wait = WebDriverWait(chrome_driver, 30)
        button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-title-shortcut="Esc"]')))
        button.click()
        pprint(list_with_message)
    chrome_driver.close()
    name_db = 'inbox_mail'
    load_data_to_mongodb(list_with_message, name_db)
