# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

sd.resolution = (1200, 800)

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

x, y = 0, 0
brick_x, brick_y = 100, 50
i = 0
for y in range(0, sd.resolution[1], brick_y):
    i += 1
    for x in range(0, sd.resolution[0], brick_x):
        if i % 2 == 1:
            x -= brick_x/2
        # x0 = x if i % 2 == 0 else x - brick_x/2
        point1 = sd.get_point(x, y)
        point2 = sd.get_point(x + brick_x, y + brick_y)
        sd.rectangle(point1, point2, width=1)

sd.pause()
