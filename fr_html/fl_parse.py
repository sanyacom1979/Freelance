import re

from bs4 import BeautifulSoup

import time

from fr_html.fr_reqv import reqv
from file_func.f_txt import to_tmp_txt
from date_time.date_time import yyyymmdd, kvo_dney
from tqdm import tqdm


def fl_parse_work(data, hdrs, f_tmp_work_det):
    base_adr = "https://www.fl.ru"
    # BeautifulSoup пакет для парсинга
    soup = BeautifulSoup(data, "html.parser")
    # Область где хранится ссылка
    work_items = soup.find_all("div", {"class" : "b-post__grid"})
    print("1-й этап парсинга...")
    time.sleep(1)
    for work_item in tqdm(work_items):
        if work_item.find("h2", {"class" : "b-post__title b-post__grid_title p-0 b-post__pin"}):
            # Закрепленная ссылка
            w_detail_lnk = work_item.find("h2", {"class" : "b-post__title b-post__grid_title p-0 b-post__pin"}).find("a").get("href")
        else:
            # Незакрепленная ссылка
            w_detail_lnk = work_item.find("h2", {"class" : "b-post__title b-post__grid_title p-0"}).find("a").get("href")
        # Скачиваем ссылку
        det_data = reqv(f"{base_adr}{w_detail_lnk}", hdrs)
        # и сохраняем во временный файл с детализацией
        to_tmp_txt(det_data, f_tmp_work_det)


def fl_parse_work_det(data, work_list, how_many_days, birza):
    # BeautifulSoup пакет для парсинга
    soup = BeautifulSoup(data, "html.parser")
    # Область, откуда я буду брать инфу по заказу
    work_items = soup.find_all("div", {"class" : "main"})
    print("2-й этап парсинга...")
    time.sleep(1)
    for work_item in tqdm(work_items):
        # Откидываем вакансии, заказы, взятые в работу. И меня интересует только безопасная сделка
        if work_item.find("div", {"class": "b-layout__txt b-layout__txt_padbot_20"}) and \
                work_item.find("div", {"class" : "b-fon b-fon_bg_f5 b-fon_pad_10 b-fon_margbot_20"}) == None and \
                work_item.find("a", {"class" : "b-layout__txt_fontsize_12 b-layout__txt_bold b-layout__txt_color_1da409 b-layout__txt_padright_5 b-layout__txt_text_decor_none"}):
            # Тема
            tema = work_item.find("h1", {"class": "b-page__title"}).text.strip()
            # Техническое задание
            tz = work_item.find("div", {"class" : "b-layout__txt b-layout__txt_padbot_20"}).text.strip()
            # Оплата и срок
            oplata_srok = work_item.find_all("div", {"class" : "b-layout__txt b-layout__txt_fontsize_18 b-layout__txt_fontsize_13_iphone"})
            oplata = oplata_srok[0].find("span", {"class" : "b-layout__bold"}).text.strip()
            if len(oplata_srok) > 1:
                srok = oplata_srok[1].find("span", {"class" : "b-layout__bold"}).text.strip()
            else:
                srok = ""
            # Инфа по заказчику
            zak_plus_otz = work_item.find_all("span", {"class" : "b-layout__txt b-layout__txt_fontsize_11 b-layout__txt_color_6db335"})
            zak_plus_otz = zak_plus_otz[1].text.strip()
            zak_minus_otz = work_item.find("span", {"class" : "b-layout__txt b-layout__txt_fontsize_11 b-layout__txt_color_c10600"}).text.strip()
            zak_na_rinke = work_item.find_all("span", {"class" : "b-layout_block_iphone"})
            zak_na_rinke = zak_na_rinke[1].text.strip()
            # Дата обновления инфы
            date_pub = work_item.find("div", {"class" : "b-layout__txt b-layout__txt_padbot_30"}).find("div", {"class" : "b-layout__txt b-layout__txt_fontsize_11"}).text.strip()
            # [0] - дата публикации, [1] - дата обновления (что меня и интересует)
            date_pub1 = re.findall("\d{2}\.\d{2}\.\d{4}", date_pub)[1]
            time_pub = re.findall("\d{2}:\d{2}", date_pub)[1]
            # При попадании заказа в диапазон - добавляем заказ в список work_list
            if kvo_dney(yyyymmdd(date_pub1)) < how_many_days:
                work_dict = {"Фриланс-Биржа" : birza.upper(), "Тема" : tema, "Тех. задание" : tz,
                            "Оплата" : oplata, "Срок" : srok, "Заказчик: +отзывы": zak_plus_otz,
                            "Заказчик: -отзывы": zak_minus_otz, "Заказчик: на рынке" : zak_na_rinke, "Дата и время публикации" : f"{date_pub1} {time_pub}"}
                work_list.append(work_dict)
    # Возвращаем список
    return work_list