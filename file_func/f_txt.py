import os

# функция записи в файл
def to_tmp_txt(data, path):
    if os.path.exists(path):
        with open(path, mode="a", encoding="utf-8") as f:
            f.write(data)
    else:
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(data)

# функция чтения из файла
def from_tmp_txt(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = f.read()
            return data
    else:
        raise FileNotFoundError(f"Файл {path} не найден")

# функция удаления файлов
def del_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"Файл {path} удален.")
    except PermissionError:
        raise PermissionError(f"Файл '{path}' уже открыт. Для удаления файл нужно закрыть.")

