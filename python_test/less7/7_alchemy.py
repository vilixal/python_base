# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())

class Water:

    def __add__(self, other):
        if str(other)=='Воздух':
            result=Storm()
        else:
            result = Flash()
        return result

    def check(self):
        param=1
        return param

    def __str__(self):
        return 'Вода'



class Air:

    def __str__(self):
        return 'Воздух'

class Storm:

    def __str__(self):
        return 'Шторм'

class Flash:

    def __str__(self):
        return 'Молния'
water=Water()
air=Air()
flash=Flash()
# print(Water(), '+', Flash(), '=', Water() + Flash())
print(water, '+', air, '=', water + flash)
if water.check()!=1:
    print(1)
else:
    print(0)




# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
