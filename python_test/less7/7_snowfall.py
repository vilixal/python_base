# -*- coding: utf-8 -*-
from random import randint

import simple_draw as sd

# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку

sd.resolution = (1200, 600)

def get_flakes(count=10,n=0):
    flakes_list = []
    for i in range(count):
        flake = Snowflake(n)
        flakes_list.append(flake)
    return flakes_list

class Snowflake:

    def __init__(self,n=0):
        self.x = randint(100,1100)
        if n!=1:
            self.y = randint(100,600)
        else:
            self.y = 600
        self.point = sd.get_point(self.x, self.y)
        self.length =randint(20,40)

    def clear_previous_picture(self):
        sd.snowflake(center=self.point, length=self.length, color=sd.background_color)


    def move(self):
        self.y -= 5+(self.length-20)/3
        self.x += randint(-10,10)

    def draw(self):
        self.point = sd.get_point(self.x, self.y)
        sd.snowflake(center=self.point, length=self.length, color=sd.COLOR_WHITE)

    def __bool__(self):
        return self.y<=self.length


# flake = Snowflake()
count=50
flakes = get_flakes(count=count)

while True:
    flakes_delta = []
    i=count-1
    for flake in flakes[count-1:0:-1]:
        if flake:
            flakes.pop(i)
        i-=1
    flakes_delta = get_flakes(count=count-len(flakes),n=1)
    flakes.extend(flakes_delta)
    sd.start_drawing()
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
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
