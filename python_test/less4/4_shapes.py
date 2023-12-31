# -*- coding: utf-8 -*-

import simple_draw as sd

# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg


# def shape(point, angle=0, form=3):  # 2 функции
#     for i in range(form):
#         point = print_vector(point, angle, i, form)
#
#
# def print_vector(point, angle, side, form):
#     v1 = sd.get_vector(start_point=point, angle=angle + 360 * ((side) / form), length=100, width=2)
#     v1.draw()
#     return v1.end_point


def shape(point, angle=0, form=3, side=0):  # рекурсия
    if side == form:
        return None
    v1 = sd.get_vector(start_point=point, angle=angle + 360 * ((side) / form), length=100, width=2)
    v1.draw()
    shape(v1.end_point, angle, form, side + 1)


length = 150
angle_0 = 45
point_1 = sd.get_point(100, 100)
point_2 = sd.get_point(100, 300)
point_3 = sd.get_point(400, 100)
point_4 = sd.get_point(400, 300)

shape(point=point_1, angle=angle_0, form=3)
shape(point=point_2, angle=angle_0, form=4)
shape(point=point_3, angle=angle_0, form=5)
shape(point=point_4, angle=angle_0, form=6)

# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44?

# Часть 2 (делается после зачета первой части)
#
# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв
#   в начальной/конечной точках рисуемой фигуры (если он есть)

# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9
# Будьте ленивыми, не используйте копи-пасту!


sd.pause()
