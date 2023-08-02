# Напишите функцию, которая создаёт из созданного ранее
# файла новый с данными в формате JSON.

import json
from pathlib import Path

def text_json(file: Path) -> None:
    file_data = {}
    with open(file, 'r', encoding="utf-8") as f:
        for line in f:
            name, number = line.split(" ")
            file_data[name.capitalize()] = float(number)
            with open(file.stem + ".json", "w") as f:
                json.dump(file_data, f, indent = 2)

if __name__ == '__main__':
    text_json(Path('file1.txt'))
# ---------------------------------------------------------------------------------------------------

# Напишите функцию, которая в бесконечном цикле
# запрашивает имя, личный идентификатор и уровень
# доступа (от 1 до 7).
# После каждого ввода добавляйте новую информацию в
# JSON файл.
# Пользователи группируются по уровню доступа.

import json
from pathlib import Path


def fill_bd(file: Path):
    current_set = set()

    if Path.exists(file):
        with open(file, 'r', encoding='utf-8') as fj:
            dict_bd = json.load(fj)
            for _, value in dict_bd.items():
                current_set.update(value.keys())
    else:
        dict_bd = {i: {} for i in range(1, 8)}
        
        current_data = input(f'введите Имя, id, уровень доступа (от 1 до 7) через пробел: \n ')
        while current_data != "":
            name, id_cod, level = current_data.split()
            if id_cod not in current_set:
                current_set.add(id_cod)
                dict_bd[int(level)] = {id_cod: name}
                
                with open(file, "w", encoding='utf-8') as fj:
                    json.dump(dict_bd, fj, indent=2, ensure_ascii=False)
                            
            current_data = input(f'введите Имя, id, уровень доступа (от 1 до 7) через пробел: \n ')

if __name__ == '__main__':
    fill_bd(Path('test_bd.json'))


# ------------------------------------------------------------------------------------------
# # Напишите функцию, которая ищет json файлы в указанной
# директории и сохраняет их содержимое в виде
# одноимённых pickle файлов.     
import os
import pickle
import csv
import json
from pathlib import Path

def from_json_to_pickle(file):
    for i in os.listdir(file):
        if i.endswith(".json"):
            with (open(i.replace(".json", ".pickle"), "wb") as pik, open(i) as js):
                pickle.dump(js.read(), pik)

if __name__ == "-_main__":
    from_json_to_pickle(Path.cwd())

# -------------------------------------------------------------------------------------------------------
# # Напишите функцию, которая получает на вход директорию и рекурсивно обходит её 
# и все вложенные директории. Результаты обхода сохраните в файлы json, csv и pickle.
# Для дочерних объектов указывайте родительскую директорию.
# Для каждого объекта укажите файл это или директория.
# Для файлов сохраните его размер в байтах, а для директорий размер файлов 
# в ней с учётом всех вложенных файлов и директорий.
import os
import json
import csv
import pickle
from pathlib import Path


def size_func(dir):
    total = 0
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in dirnames:
            filepath = os.path.join(dirpath, f)
            total += os.path.getsize(filepath)
    return total

def run_by_directory(path_direcion):
    data = []
    for dirpath, dirnames, filenames in os.walk(path_direcion):
        for name in dirnames:
            f_path = os.path.join(dirpath, name)
            size = size_func(f_path)
            data.append({"parent_dir": dirpath, 
                            "type": 'directory',
                            "name": name,
                            "size_bytes": size
                            })

        for name in filenames:
            full_path = os.path.join(dirpath, name)
            size = os.path.getsize(full_path)
            data.append({"parent_directory": dirpath, 
                            "type": 'file',
                            "name": name,
                            "size_bytes": size})

    with(open("directory_data.json", "w") as json_file,
         open("directory_data.csv", "w", newline='') as csv_file, 
         open('directory_data_pickle', 'wb') as pickle_file):
        
        json.dump(data, json, indent=20)

        f_name = ['parent_directory', 'type', 'name', 'size_bytes']
        dir_wr = csv.DictWriter(csv_file, f_name=f_name)
        dir_wr.writeheader()
        dir_wr.writerows(data)

        pickle.dump(data, pickle_file)

if __name__ == "-_main__":
    run_by_directory(Path.cwd())                  
