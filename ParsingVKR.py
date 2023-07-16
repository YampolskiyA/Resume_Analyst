
import csv
import re
import requests

from time import sleep
from urllib.parse import quote_plus
from lxml import html


def query(text, resume=False):
    """
    Парсинг страницы поиска
    """
    text = quote_plus(text.lower())
    url = "https://hh.ru/search/"

    if resume:
        url += "resume?area=1&logic=normal&pos=full_text&exp_period=all_time&st=resumeSearch&text=" + text
        rx = "//h1/div/span"
    else:
        url += "vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=" + text
        rx = "//h1"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/96.0.4664.174 YaBrowser/22.1.4.840 Yowser/2.5 Safari/537.36', }

    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok: raise Exception(f"http code == {r.status_code}")
    if not r.content or len(r.content) < 7: raise Exception(f"no content at {url}")

    el = html.fromstring(r.content.decode('utf-8')).xpath(rx)

    if el:
        counter_text = el[0].text_content().split("ваканс")[0]
        count = re.sub(r'[^0-9]', '', counter_text)
        count = 0 if len(count) < 1 else int(count)
    else:
        count = 0

    print([key, text, count], sep=";")

    return count


def save(text, vacancies=0, people=0):
    '''
    Запись в файл
    '''
    text = text.lower()
    filename = "data.csv"

    data = {}
    for i in csv.reader(open(filename, 'r', encoding='UTF8')):
        if len(i) > 2: data[i[0]] = i

    data[text] = [text, vacancies, people]

    writer = csv.writer(open(filename, 'w', encoding='UTF8', newline=''))
    writer.writerows(data.values())


keys = "excel,git,sql,mysql," \
       "python,numpy,ООП,c++,scala,matlab,r,sas,яндекс.метрика, google analytics," \
       "power bi,tableau,matplotlib,pandas,базы данных,математическая статистика"

for key in keys.split(","):
    vacancies = query(key, resume=False)
    sleep(2)
    people = query(key, resume=True)
    save(key, vacancies, people)
    sleep(3)
