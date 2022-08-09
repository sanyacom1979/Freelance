from file_func.f_txt import del_file
from fr_html.fl_parse import fl_parse_work, fl_parse_work_det
from fr_html.weblancer_parse import webl_parse_work, webl_parse_work_det
from fr_html.fr_common import common
from excel.excel import to_excel

# Итоговая табличка
f_excel = "excel/results.xlsx"
# временные файлы, куда будут загружаться странички
f_tmp_work = "fr_html/tmp_work.txt"
f_tmp_work_det = "fr_html/tmp_w_det.txt"
print(f"Сначала удаляем итоговую табличку при наличии")
del_file(f_excel)

how_many_days = int(input("За сколько дней собирать?"))

fr_dict = {"fl.ru" : ("https://www.fl.ru/projects/category/programmirovanie/?page={i}&kind=5", fl_parse_work, fl_parse_work_det),
           "weblancer.net" : ("https://www.weblancer.net/jobs/veb-programmirovanie-31/?page={i}", webl_parse_work, webl_parse_work_det)}

work_list = []  # список для инфы по заказам со всех фриланс-бирж

# Для иммитации входа с браузера
hdrs = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

# n первых страниц
n = 10

# Обрабатывааем по очереди фриланс-биржы из словарика "fr_dict"
for k, v in fr_dict.items():
    start_adr, f_parse, f_parse_det = v
    work_list = common(k, start_adr, f_parse, f_parse_det, work_list, hdrs, n, how_many_days, f_tmp_work, f_tmp_work_det)

# загружаем список work_list в excel
print(f"Запись результатов в {f_excel}...")
to_excel(work_list, f_excel)