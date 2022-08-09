import re

from bs4 import BeautifulSoup

import time

from fr_html.fr_reqv import reqv
from file_func.f_txt import to_tmp_txt
from date_time.date_time import yyyymmdd, kvo_dney
from tqdm import tqdm

def webl_parse_work(data, hdrs, f_tmp_work_det):
    base_adr = "https://www.weblancer.net"
    # BeautifulSoup пакет для парсинга
    soup = BeautifulSoup(data, "html.parser")
    # Область где хранится ссылка
    work_items = soup.find_all("div", {"class": "row click_container-link set_href"})
    print("1-й этап парсинга...")
    time.sleep(1)
    for work_item in tqdm(work_items):
    # откидываем заказы, где исполнитель определен
        if work_item.find("div", {"class" : "text-success"}) == None:
            w_detail_lnk = work_item.find("a").get("href")
            # Скачиваем ссылку
            det_data = reqv(f"{base_adr}{w_detail_lnk}", hdrs)
            # и сохраняем во временный файл с детализацией
            to_tmp_txt(det_data, f_tmp_work_det)



def webl_parse_work_det(data, work_list, how_many_days, birza):
    # BeautifulSoup пакет для парсинга
    soup = BeautifulSoup(data, "html.parser")
    # Область, откуда я буду брать инфу по заказу
    work_items = soup.find_all("div", {"class" : "main-wrapper"})
    print("2-й этап парсинга...")
    time.sleep(1)
    for work_item in tqdm(work_items):
        # Тема
        tema = work_item.find("div", {"class": "col page_header_content"}).find("h1").text.strip()
        # Техническое задание
        # без авторизации
        if work_item.find("div", {"class": "col-12 text_field"}):
            tz = work_item.find("div", {"class": "col-12 text_field"}).find("p").text.strip()
        # Оплата
            if work_item.find("span", {"class" : "title amount"}):
                oplata = work_item.find("span", {"class" : "title amount"}).text.strip()
            else:
                oplata = ""
        # По срокам инфы нет
            srok = ""
        # Инфа по заказчику
            if re.findall("<span>\d+ отз\w+", str(work_item)):
                zak_plus_otz = re.findall("<span>\d+ отз\w+", str(work_item))[0]
                zak_plus_otz = re.findall("\d+", zak_plus_otz)[0]
                zak_plus_otz = "+ " + zak_plus_otz
            else:
                zak_plus_otz = "+ 0"
            if work_item.find("span", {"class": "text-danger ms-1"}):
                zak_minus_otz = work_item.find("span", {"class" : "text-danger ms-1"}).text.strip()
                zak_minus_otz = zak_minus_otz[1:-1]
            else:
                zak_minus_otz = "- 0"
            zak_na_rinkes = work_item.find_all("div", {"class" : "text-muted"})
            zak_na_rinke = zak_na_rinkes[1].text.strip()
        # Дата обновления инфы
            date_pub = work_item.find("div", {"class" : "float-right text-muted hidden-xs-down"}).find("span").get("title")
            date_pub1 = re.findall("\d{2}\.\d{2}\.\d{4}", date_pub)[0]
            time_pub = re.findall("\d{2}:\d{2}", date_pub)[0]
            # При попадании заказа в диапазон - добавляем заказ в список work_list
            if kvo_dney(yyyymmdd(date_pub1)) < how_many_days:
                work_dict = {"Фриланс-Биржа": birza, "Тема": tema, "Тех. задание": tz,
                             "Оплата": oplata, "Срок": srok, "Заказчик: +отзывы": zak_plus_otz,
                             "Заказчик: -отзывы": zak_minus_otz, "Заказчик: на рынке": zak_na_rinke,
                             "Дата и время публикации": f"{date_pub1} {time_pub}"}
                work_list.append(work_dict)
                # Возвращаем список
    return work_list