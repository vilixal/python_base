from random import randint

number = '0'


def guess_number():
    global number
    number = str(randint(1000, 9999))
    return number


def check_number(num):
    res = {'bulls': 0, 'cows': 0}
    i = 0
    for number_i in number:
        if number_i == num[i]:
            res['bulls'] += 1
        elif number_i in num:
            res['cows'] += 1
        i += 1
    # i, j = 0, 0
    # for numi in num:
    #     j = 0
    #     if num[i] == number[i]:
    #         res['bulls'] += 1
    #         i += 1
    #         continue
    #     for numberi in number:
    #         if numi == numberi and i != j and num[j] != number[j]:
    #             res['cows'] += 1
    #             break
    #         j += 1
    #     i += 1
    return res
