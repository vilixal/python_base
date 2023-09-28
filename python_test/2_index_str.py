#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть строка с перечислением фильмов

my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

# Выведите на консоль с помощью индексации строки, последовательно:
#   первый фильм
#   последний
#   второй
#   второй с конца
first_zp = my_favorite_movies.find(',')
second_zp = my_favorite_movies.find(',', first_zp + 1)
thirst_zp = my_favorite_movies.find(',', second_zp + 1)
for_zp = my_favorite_movies.find(',', thirst_zp + 1)
first_filt = my_favorite_movies[:first_zp]
last_film = my_favorite_movies[for_zp + 2:]
second_film = my_favorite_movies[first_zp + 2:second_zp]
for_film = my_favorite_movies[thirst_zp + 2:for_zp]
print(first_filt)
print(last_film)
print(second_film)
print(for_film)

# Переопределять my_favorite_movies и использовать .split() нельзя.
# Запятая не должна выводиться.

