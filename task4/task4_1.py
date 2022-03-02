import requests
from lxml import html
from pprint import pprint
import re
from datetime import datetime
from pymongo import MongoClient


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


def list_to_str(list_str):
    """Функция преобразует список строк в одну строку"""
    if len(list_str) > 1:
        str_out = list_str[0] + '. '
        for i in list_str[1:]:
            str_out += i
    else:
        str_out = list_str[0]
    return str_out


def info_topnews_from_lenta_ru():
    """Функция собирает информацию(название источника,наименование новости,ссылку на новость,
        дату публикации) с сайта lenta.ru и сохраняет в список"""
    topnews_list = list()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    url ='https://lenta.ru/'
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    items = dom.xpath("//a[@class='card-big _topnews _news' or @class = 'card-mini _topnews']")
    for item in items:
        item_info = dict()
        info = item.xpath(".//h3/text() | .//span[@class='card-mini__title']/text()")[0]
        link = item.xpath("./@href")[0]
        if 'http' not in link:
            link = url + link[1:]
            response_1 = requests.get(link, headers=headers)
            dom_1 = html.fromstring(response_1.text)
            date = dom_1.xpath("//time[@class='topic-header__item topic-header__time']/text()")[0]
            date_str =date[7:] + ' ' + date[:5]
            date_str = int_value_from_ru_month(date_str)
            date_time = datetime.strptime(date_str, '%d %m %Y %H:%M')
            news_source = url
        else:
            time = item.xpath(".//time[@class='card-big__date' or @class = 'card-mini__date']/text()")[0]
            date = re.findall(r'\b(\d+.\d+.\d+)\b', link)[0]
            date_str = date + ' ' + time
            date_time = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
            news_source = link[link.find('.'):]
            news_source = link[:link.find('.')] + news_source[:news_source.find('/')+1]
        item_info['info'] = info
        item_info['link'] = link
        item_info['date_time'] = date_time.strftime('%d %B %Y, %H:%M:%S')
        item_info['news_source'] = news_source
        topnews_list.append(item_info)
    return topnews_list


def info_topnews_from_news_mail_ru():
    """Функция собирает информацию(название источника,наименование новости,ссылку на новость,
    дату публикации) с сайта news.mail.ru и сохраняет в список"""
    topnews_list = list()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    url ='https://news.mail.ru/'
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    items = dom.xpath("//div[@data-logger='news__MainTopNews']//div[contains(@class, 'daynews__item')]"
                      " | //div[@data-logger='news__MainTopNews']//li[contains(@class, 'list__item')]")
    for item in items:
        item_info = dict()
        info = list_to_str(item.xpath(".//span/span/text() | ./a/text()")).replace('\xa0', ' ')
        link = item.xpath(".//@href")[0]
        response_1 = requests.get(link, headers=headers)
        dom_1 = html.fromstring(response_1.text)
        date = dom_1.xpath("//div[contains(@class, 'article js-article')]//span[@datetime]/@datetime")[0]
        news_source = dom_1.xpath("//div[contains(@class, 'article js-article')]//a/@href")[0]
        date_time = datetime.strptime(date[:date.find('+')], '%Y-%m-%dT%H:%M:%S')
        item_info['info'] = info
        item_info['link'] = link
        item_info['date_time'] = date_time.strftime('%d %B %Y, %H:%M:%S')
        item_info['news_source'] = news_source
        topnews_list.append(item_info)
    return topnews_list


def add_inform_to_db(lisp_in, db_n):
    """Функция записывает собранные новости из списка в БД"""
    for item in lisp_in:
        if db_n.count_documents({'link': item['link']}) == 0:
            db_n.insert_one(item)


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['news_db']
    news = db.news
    news.drop()
    add_inform_to_db(info_topnews_from_lenta_ru() + info_topnews_from_news_mail_ru(), news)
    for doc in news.find({}):
        pprint(doc)
