# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

sd.resolution = (800, 800)

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

x, y = 0, 0
i = 0
for y in range(0, 850, 50):
    if i == 1:
        i -= 1
    else:
        i += 1
    for x in range(0, 850, 100):
        if i == 1:
            x -= 50
        point1 = sd.get_point(x, y)
        point2 = sd.get_point(x + 100, y + 50)
        sd.rectangle(point1, point2, width=2)

sd.pause()
