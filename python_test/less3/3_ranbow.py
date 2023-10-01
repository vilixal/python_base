# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

sd.resolution = (800, 800)
rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)
# x, y = 50, 50
# x1, y1 = 350, 450
# i = 0
# for i in range(7):
#     point1 = sd.get_point(x, y)
#     point2 = sd.get_point(x1, y1)
#     sd.line(point1, point2, rainbow_colors[i], 4)
#     x += 5
#     x1 += 5

# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво
x, y = 400, -200
radius = 600
step = 10
for i in range(7):
    point1 = sd.get_point(x, y)
    sd.circle(point1, radius, rainbow_colors[i], 10)
    radius -= step

sd.pause()
