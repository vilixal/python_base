# -*- coding: utf-8 -*-
from random import randint

import simple_draw as sd

# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку

sd.resolution = (1200, 600)


class Snowflake:

    def __init__(self):
        self.x = 500
        self.y = 500
        self.point = sd.get_point(self.x, self.y)

    def clear_previous_picture(self):
        sd.snowflake(center=self.point, length=50, color=sd.background_color)


    def move(self):
        self.y -= 10
        self.x += randint(-10,10)

    def draw(self):
        self.point = sd.get_point(self.x, self.y)
        sd.snowflake(center=self.point, length=50, color=sd.COLOR_WHITE)

def get_flakes(count=10):
    flakes_list = []
    for i in range(count):
        flake = Snowflake()
        flakes_list.append(flake)
    return flakes_list




flake = Snowflake()
# flakes = get_flakes(count=N)

while True:
    sd.start_drawing()
    flake.clear_previous_picture()
    flake.move()
    flake.draw()
    # if not flake.can_fall():
    #     break
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
# flakes = get_flakes(count=N)  # создать список снежинок
# while True:
#     for flake in flakes:
#         flake.clear_previous_picture()
#         flake.move()
#         flake.draw()
#     fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
#     if fallen_flakes:
#         append_flakes(count=fallen_flakes)  # добавить еще сверху
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

sd.pause()
