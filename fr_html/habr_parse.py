import re

from bs4 import BeautifulSoup

import time

from fr_html.fr_reqv import reqv
from file_func.f_txt import to_tmp_txt
from date_time.date_time import kvo_dney, conv_month_num
from tqdm import tqdm



def habr_parse_work(data, hdrs, f_tmp_work_det):
    base_adr = "https://freelance.habr.com"
    # BeautifulSoup пакет для парсинга
    soup = BeautifulSoup(data, "html.parser")
    # Область где хранится ссылка
    work_items = soup.find_all("li", {"class": "content-list__item"})
    print("1-й этап парсинга...")
    time.sleep(1)
    for work_item in tqdm(work_items):
        # заказы, где исполнитель определен видимо на страничке не отображаются
        # поэтому откидываем только, где нет безопасной сделки
        if work_item.find("span", {"class": "safe-deal-icon"}):
            w_detail_lnk = work_item.find("div", {"class" : "task__title"}).find("a").get("href")
            # Скачиваем ссылку
            det_data = reqv(f"{base_adr}{w_detail_lnk}", hdrs)
            # и сохраняем во временный файл с детализацией
            to_tmp_txt(det_data, f_tmp_work_det)


def habr_parse_work_det(data, work_list, how_many_days, birza):
    # BeautifulSoup пакет для парсинга
    soup = BeautifulSoup(data, "html.parser")
    # Область, откуда я буду брать инфу по заказу
    work_items = soup.find_all("div", {"class": "layout"})
    print("2-й этап парсинга...")
    time.sleep(1)
    for work_item in tqdm(work_items):
        # Тема
        tema = work_item.find("h2", {"class": "task__title"}).text.strip()
        tema = tema[:tema.index("\n\n")] + " " + tema[tema.index("\n\n") + 2:]
        # Техническое задание
        tz = work_item.find("div", {"class": "task__description"}).text.strip()
        # Оплата
        oplata = work_item.find("div", {"class": "task__finance"}).text.strip()
        # По срокам инфы нет
        srok = ""
        # Инфа по заказчику
        zak = work_item.find_all("div", {"class" : "value"})
        zak_otz = zak[3].find_all("a")
        zak_plus_otz = zak_otz[0].text.strip()
        zak_plus_otz = f"{zak_plus_otz[0]} {zak_plus_otz[1]}"
        zak_minus_otz = zak_otz[1].text.strip()
        zak_minus_otz = f"{zak_minus_otz[0]} {zak_minus_otz[1]}"
        zak_na_rinke = zak[4].text.strip()
        # Дата обновления инфы
        date_pub = work_item.find("div", {"class": "task__meta"}).text.strip()
        date_pub1 = re.findall("\d{2} \w+ \d{4}", date_pub)[0]
        date_pub1 = f"{date_pub1[:2]}.{conv_month_num(date_pub1[3:-5].lower())}.{date_pub1[-4:]}"
        time_pub = re.findall("\d{2}:\d{2}", date_pub)[0]
        # При попадании заказа в диапазон - добавляем заказ в список work_list
        if kvo_dney(date_pub1) < how_many_days:
            work_dict = {"Фриланс-Биржа": birza.upper(), "Тема": tema, "Тех. задание": tz,
                         "Оплата": oplata, "Срок": srok, "Заказчик: +отзывы": zak_plus_otz,
                         "Заказчик: -отзывы": zak_minus_otz, "Заказчик: на рынке": zak_na_rinke,
                         "Дата и время публикации": f"{date_pub1} {time_pub}"}
            work_list.append(work_dict)
        # Возвращаем список
    return work_list