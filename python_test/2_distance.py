#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов
from pprint import pprint
sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - корень из (x1 - x2) ** 2 + (y1 - y2) ** 2

distances = {}
moscow=sites['Moscow']
london=sites['London']
paris=sites['Paris']
moscow_london=((moscow[0]-london[0])**2 + (moscow[1]-london[1])**2)**0.5
moscow_paris=((moscow[0]-paris[0])**2 + (moscow[1]-paris[1])**2)**0.5
distances['Москва']={}
distances['Москва']['Лондон']=moscow_london
distances['Москва']['Париж']=moscow_paris

paris_london=((paris[0]-london[0])**2 + (paris[1]-london[1])**2)**0.5
distances['Лондон']={}
distances['Лондон']['Москва']=moscow_london
distances['Лондон']['Париж']=paris_london

distances['Париж']={}
distances['Париж']['Москва']=moscow_paris
distances['Париж']['Лондон']=paris_london

pprint(distances)
