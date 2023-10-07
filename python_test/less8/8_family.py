# -*- coding: utf-8 -*-

from colorama import Fore, init
init(autoreset=True)
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.dirt = 0
        self.safe = 100
        self.food = 50

    def __str__(self):
        return 'Дома денег {} еды {} грязи {}'.format(self.safe,self.food,self.dirt)

class Man:
    fullness=30
    happi = 100

    def __init__(self, name):
        self.name = name
        self.money = 0

    def eat(self, house, food):
        self.fullness += food
        self.house.food -= food
        print('{} съел еды {}. Сытость {}'.format(self.name,food,self.fullness))

    def __str__(self):
        return '{} сытость {} счастье {}'.format(self.name,self.fullness,self.happi)


class Husband(Man):

    def __init__(self, name, house):
        super().__init__(name=name)
        self.house = house
        self.money = 0

    def __str__(self):
        return super().__str__()

    def act(self,house):
        if self.money >= 150:
            self.house.safe +=150
            self.money -= 150
            print('{} положил 150 в сейф'.format(self.name))
        if self.fullness <= 10:
            self.eat(house,30)
        elif self.happi <=20:
            self.gaming()
        elif self.house.safe <=50:
            self.work()
        else:
            self.work()

    def work(self):
        cash = 100
        self.money += cash
        self.fullness -= 10
        self.happi -=10
        print('{} пошел на работу и заработал {}'.format(self.name,cash))

    def gaming(self):
        self.fullness -= 10
        self.happi += 20
        print('{} поиграл в WOT'.format(self.name))


class Wife(Man):

    def __init__(self, name, house):
        super().__init__(name=name)
        self.house = house
        self.money = 0

    def __str__(self):
        return super().__str__()

    def act(self,house):
        if self.fullness <= 10:
            self.eat(house,30)
        elif self.happi <=40:
            if house.money + self.money < 350:
                grab_money = self.house.money
                self.money += grab_money
                self.house.money = 0
                print('{} взяла из сейфа деньги {} на будущую шубу'.format(self.name, grab_money))
            else:
                self.buy_fur_coat(house)
        elif self.house.food <=60:
            self.shopping(house)
        else:
            self.eat(house, 30)



    def shopping(self,house):
        grab_money = 100 - self.money
        self.money += grab_money
        self.house.safe -= grab_money
        self.house.food += 100
        self.money -= 100
        print('{} взяла {} из сейфа и купила 100 еды'.format(self.name, grab_money))


    def buy_fur_coat(self,house):
        grab_money = 60 - self.money
        self.money += grab_money
        self.house.safe -= grab_money
        print('{} взяла {} из сейфа и купила шубу'.format(self.name,grab_money))

    def clean_house(self):
        pass


home = House()
serge = Husband('Сережа',home)
masha = Wife('Маша',home)

for day in range(365):
    print(Fore.GREEN + '================== День {} =================='.format(day))
    serge.act(home)
    masha.act(home)
    print(Fore.YELLOW + str(serge))
    print(Fore.YELLOW + str(masha))
    print(Fore.YELLOW + str(home))


######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


# class Cat:
#
#     def __init__(self):
#         pass
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#     def soil(self):
#         pass


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)
#
# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.
#
#
# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

