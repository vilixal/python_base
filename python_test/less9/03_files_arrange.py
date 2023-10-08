# -*- coding: utf-8 -*-

import os, time, shutil
import zipfile
from pprint import pprint

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

def create_dir(cdir, rec='delete'):
    if os.path.exists(cdir) and rec == 'delete':
        shutil.rmtree(cdir)
        os.makedirs(cdir)
    elif os.path.exists(cdir) is not True:
        os.makedirs(cdir)


zip_name = 'icons.zip'
temp_dir = 'extract'
sorted_dir = 'sorted_dir'
sort = []
create_dir(temp_dir)
with zipfile.ZipFile(zip_name, 'r') as zf:
    for file in zf.infolist():
        file_name = os.path.basename(file.filename)
        # file_path = os.path.normpath(file.filename)
        file_date = list(file.date_time)
        if len(str(file_date[1])) == 1:
            file_date[1] = '0' + str(file_date[1])
        if file.is_dir() is not True:
            sort.append([file_name, file_date])
        zf.extract(file, path=temp_dir)
    print(sort)

create_dir(sorted_dir)

for dirpath, dirnames, filenames in os.walk(temp_dir):
    print(dirpath, dirnames, filenames)

    for file in filenames:
        full_file_path = os.path.join(dirpath, file)
        print(full_file_path)
        for filedata in sort:
            if filedata[0] == file:
                full_new_path = os.path.join(sorted_dir, str(filedata[1][0]), str(filedata[1][1]))
                create_dir(full_new_path, 'add')
                shutil.copy2(full_file_path, full_new_path)





# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Основная функция должна брать параметром имя zip-файла и имя целевой папки.
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
