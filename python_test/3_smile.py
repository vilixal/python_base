# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd


# Написать функцию отрисовки смайлика в произвольной точке экрана
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.
def smile(x, y, color):
    size = 50
    point1 = sd.get_point(x - size, y - size * 3 / 4)
    point2 = sd.get_point(x + size, y + size * 3 / 4)
    point3 = sd.get_point(x - size / 3, y + size / 4)
    point4 = sd.get_point(x + size / 3, y + size / 4)
    point5 = sd.get_point(x - size * 2 / 3, y - size / 10)
    point6 = sd.get_point(x - size / 5, y - size / 3)
    point7 = sd.get_point(x + size / 5, y - size / 3)
    point8 = sd.get_point(x + size * 2 / 3, y - size / 10)
    sd.ellipse(point1, point2, color=color, width=1)
    sd.circle(point3, radius=size / 10, color=color)
    sd.circle(point4, radius=size / 10, color=color)
    sd.lines([point5, point6, point7, point8], color=color)


# size = input('Размер смайла (рекомендованный 50): ')
for _ in range(10):
    point = sd.random_point()
    x, y = point.x, point.y
    color = sd.random_color()
    smile(x, y, color)

sd.pause()
