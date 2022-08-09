from datetime import datetime
# Форматирование даты в "YYYY-MM-DD"
def yyyymmdd(dt):
    return dt[6:] + "-" + dt[3:5] + "-" + dt[:2]
# Разница в днях
def kvo_dney(dt):
    return (datetime.now() - datetime.strptime(dt, "%Y-%m-%d")).days
