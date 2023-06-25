#Написать приложение, которое собирает основные новости с сайта на выбор
# news.mail.ru, lenta.ru, dzen-новости. Для парсинга использовать XPath.
# Структура данных должна содержать:
#название источника;
#наименование новости;
#ссылку на новость;
#дата публикации.
#Сложить собранные новости в БД
#Минимум один сайт, максимум - все три


import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

url = 'https://lenta.ru/'


def get_news(url, headers):
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news = dom.xpath("//div[@class='card-mini__text']")
    news_list = []

    for new in news:
        new_dict = {}
        name_portal = url
        name = new.xpath(".//div[@class='card-mini__text']/span/text()")[0]
        link = new.xpath(".//div[@class='card-mini__text']/../@href")[0]
        date_view = new.xpath(".//div[@class='card-mini__text']/div/time/text()")[0]

        new_dict['name_portal'] = name_portal
        new_dict['name'] = name
        new_dict['link'] = link
        new_dict['date_view'] = f'{datetime.date.today()} {date_view}'

        news_list.append(new_dict)
    return news_list, url[8:13]

def load_data_to_mongodb(data, name):
    client = MongoClient(
        f"mongodb+srv://evgeny_varlamov92:27Fifa2010@cluster0.pnfwt.mongodb.net/{name}?retryWrites=true&w=majority")
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

if __name__ == "__main__":
    data, name = get_news(url, headers)
    print(data, name)
    load_data_to_mongodb(data, name)'}

url = 'https://lenta.ru/'


def get_news(url, headers):
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news = dom.xpath("//div[@class='card-mini__text']")
    news_list = []

    for new in news:
        new_dict = {}
        name_portal = url
        name = new.xpath(".//div[@class='card-mini__text']/span/text()")[0]
        link = new.xpath(".//div[@class='card-mini__text']/../@href")[0]
        date_view = new.xpath(".//div[@class='card-mini__text']/div/time/text()")[0]

        new_dict['name_portal'] = name_portal
        new_dict['name'] = name
        new_dict['link'] = link
        new_dict['date_view'] = f'{datetime.date.today()} {date_view}'

        news_list.append(new_dict)
    return news_list, url[8:13]

def load_data_to_mongodb(data, name):
    client = MongoClient(
        f"mongodb+srv://evgeny_varlamov92:27Fifa2010@cluster0.pnfwt.mongodb.net/{name}?retryWrites=true&w=majority")
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

if __name__ == "__main__":
    data, name = get_news(url, headers)
    print(data, name)
    load_data_to_mongodb(data, name)