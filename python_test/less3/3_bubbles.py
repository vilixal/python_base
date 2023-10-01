# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)
def bubble (point,step):
    radius = 50
    for _ in range(3):
        sd.circle(point, radius)
        radius += step

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей

# for _ in range(3):
#     sd.circle(point, radius)
#     radius+=5

# Написать функцию рисования пузырька, принммающую 2 (или более) параметра: точка рисовании и шаг
step = 5
# for _ in range(3):
#     sd.circle(point, radius)
#     radius+=step

# Нарисовать 10 пузырьков в ряд
# for x in range(100,1100,100):
#     point = sd.get_point(x, 100)
#     radius = 50
#     for _ in range(3):
#         sd.circle(point, radius)
#         radius+=step

# Нарисовать три ряда по 10 пузырьков
# for y in range(100, 400, 100):
#     for x in range(100, 1100, 100):
#         point = sd.get_point(x, y)
#         radius = 50
#         for _ in range(3):
#             sd.circle(point, radius)
#             radius += step

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
for _ in range(100):
    point = sd.random_point()
    bubble(point,5)

sd.pause()
