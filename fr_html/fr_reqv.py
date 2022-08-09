import requests


# Функция формирования запроса к бирже фриланса

def reqv(v_http, hdrs):
    try:
        r_http = requests.get(v_http, headers=hdrs)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError(f"Запрос к {v_http} выполнить не удалось. Проверьте подключение к интернету.")
    else:
        return r_http.text
