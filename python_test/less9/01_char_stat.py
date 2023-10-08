# -*- coding: utf-8 -*-
from pprint import pprint


# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

def print_stat(stat_sorted):
    global char, count
    print('+{txt:-^9}+{txt:-^9}+'.format(txt='-'))
    print('|{txt:^9}|{txt2:^9}|'.format(txt='буква', txt2='частота'))
    print('+{txt:-^9}+{txt:-^9}+'.format(txt='-'))
    for char, count in stat_sorted:
        print(f'|{char:^9}|{count:^9}|')
    print('|{txt:-^9}|{txt:-^9}|'.format(txt='+'))


stat = {}
with open('python_snippets\\voyna-i-mir.txt', 'r', encoding='cp1251') as file:
    for line in file:
        for char in line:
            if char.isalpha():
                if char in stat:
                    stat[char] += 1
                else:
                    stat[char] = 1
# pprint(stat)


# stat_sorted_key = sorted(stat.items())
# print_stat(stat_sorted_key)
# stat_sorted_revers = sorted(stat.items(), reverse=True)
# print_stat(stat_sorted_revers)
# stat_sorted_value = sorted(stat.items(), key=lambda item: item[1]) # https://pythonru.com/osnovy/vozmozhnosti-i-primery-funkcii-sorted-v-python
# print_stat(stat_sorted_value)

def sort_key(e):
    return e[1]

print_stat(sorted(stat.items(),key=sort_key))

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
