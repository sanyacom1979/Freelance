from datetime import datetime


# Форматирование даты в "YYYY-MM-DD"
def yyyymmdd(dt):
    return dt[6:] + "-" + dt[3:5] + "-" + dt[:2]


# Разница в днях
def kvo_dney(dt):
    return (datetime.now() - datetime.strptime(dt, "%Y-%m-%d")).days


# Преобразование месяца в номер
def conv_month_num(mon):
    m_dict = {"января" : "01", "февраля" : "02", "марта" : "03", "апреля" : "04", "мая" : "05", "июня" : "06",
              "июля" : "07", "августа" : "08", "сентября" : "09", "октября" : "10", "ноября" : "11", "декабря" : "12"}
    return m_dict[mon]