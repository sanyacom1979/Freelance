import time

from fr_html.fr_reqv import reqv
from file_func.f_txt import to_tmp_txt, from_tmp_txt, del_file
from tqdm import tqdm

def common(birza, start_adr, f_parse, f_parse_det, work_list, hdrs, n, how_many_days, f_tmp_work, f_tmp_work_det):
    print(f"ФРИЛАНС-БИРЖА - {birza.upper()}:")
    print("Сначала грубый отбор")
    print(f"Скачиваем {n} первых страниц в категории 'Программирование' во временный файл {f_tmp_work}")
    time.sleep(1)
    for i in tqdm(range(1, n + 1)):
        # в url меняем {i} на номер страницы
        start_adr1 = start_adr[:start_adr.index("{i}")] + str(i) + start_adr[start_adr.index("{i}") + 3:]
        fr_data = reqv(start_adr1, hdrs)
        to_tmp_txt(fr_data, f_tmp_work)

    print(f"Загружаем данные с временного файла {f_tmp_work}...")
    data_work = from_tmp_txt(f_tmp_work)

    # 1-й этап парсинга, скачиваем ссылки с детализацией с каждой загруженной странички
    f_parse(data_work, hdrs, f_tmp_work_det)

    print(f"Загружаем данные с временного файла {f_tmp_work_det}...")
    data_det = from_tmp_txt(f_tmp_work_det)

    # 2-й этап парсинга получение нужных данных и сохранение в список work_list
    work_list = f_parse_det(data_det, work_list, how_many_days, birza)

    print(f"Удаляем временные файлы {f_tmp_work} и {f_tmp_work_det}...")
    del_file(f_tmp_work)
    del_file(f_tmp_work_det)
    return work_list