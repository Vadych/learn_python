import os
import tempfile
import argparse
import json

storage_path = os.path.join(tempfile.gettempdir(), "storage.data")
# Проверяем наличие файла и создаем при необходимости
if not os.path.exists(storage_path):
    with open(storage_path, "w") as f:
        f.write("{}")

# Разбираем аргументы
my_parser = argparse.ArgumentParser(prefix_chars='-')
my_parser.add_argument('--key', default=False)
my_parser.add_argument('--val', default=False)
my_argument = my_parser.parse_args()
#print (my_argument.key, my_argument.val)
if my_argument.key and my_argument.val:
    #оба аргумента заданы. Добавляем в файл
    with open(storage_path,"r")as f:

        my_dict=json.load(f)
        #print(my_dict)
        if not my_argument.key in my_dict:
            my_dict[my_argument.key]=[]
        my_dict[my_argument.key].append(my_argument.val)
        #print(my_dict)
    with open(storage_path,"w")as f:
        json.dump(my_dict,f)
elif my_argument.key:
    # Val не задан. Ищем
    with open(storage_path,"r") as f:
        my_dict = json.load(f)
        if my_argument.key in my_dict:
            print(*my_dict[my_argument.key],sep=', ')
