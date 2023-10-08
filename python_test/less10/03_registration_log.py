# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

import re

class NotNameError(Exception):
    pass

class NotEmailError(Exception):
    pass

def check(line):
    name,email,age=line.split(' ')
    if name.isalpha() is not True:
        raise NotNameError
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    # pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern,email) is None:
        raise NotEmailError
    if 10 >= int(age) >= 99 is not True:
        raise ValueError('Неверный возраст')


with open('registrations.txt','r',encoding='utf8') as file:
    count=0
    for line in file:
        line=line.strip()
        count+=1
        try:
            check(line)
        except NotNameError as ext:
            print(f'{count}: В строке "{line}" возникло исключение NotNameError: "Имя содержит посторонние символы"')
        except NotEmailError as ext:
            print(f'{count}: В строке "{line}" возникло исключение NotEmailError: "Некорретный email"')
        except ValueError as ext:
            if 'unpack' in ext.args[0]:
                print(f'{count}: В строке "{line}" возникло исключение ValueError:{ext}')
            else:
                print(f'{count}: В строке "{line}" возникло исключение ValueError: "Некорретный возвраст"')