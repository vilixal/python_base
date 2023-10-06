import datetime as dt

date1 = dt.date(2022, 8, 22)
date2 = dt.date(2022, 10, 6)
date3 = dt.date(2022, 10, 14)
date4 = dt.date(2022, 10, 24)
date5 = dt.date(2023, 4, 19)
plan = {date1: 36000000, date2: 2700000, date3: 7140000, date4: 4375000, date5: -50215000}

date_s1 = dt.date(2022, 7, 10)
date_s2 = dt.date(2022, 9, 19)
stavka1, stavka2 = 8, 7.5
stavka_list = {date_s1: stavka1, date_s2: stavka2}

ratio_base = 1.0
ratio_izm = 0.9
date_start = dt.date(2022, 10, 1)
date_end = dt.date(2022, 12, 31)

fatherly_year = 2023
fatherly_month = 4

date = date1

subsidies_day, subsidies_month, subsidies_next_month, subsidies, dolg, stavka, stavka_day, subsidies_year, subsidies_next_year, ratio = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
while date <= date5:
    subsidies_day, dolg, stavka_day = 0, 0, 1
    # расчет долга за день
    for date_operation, operation in plan.items():
        if date_operation < date:
            dolg += operation
    # расчет коэффициента за день
    if date_start <= date <= date_end:
        ratio = ratio_izm
    else:
        ratio = ratio_base
    # расчет ставки за день
    for date_operation, stavka in stavka_list.items():
        if date_operation < date:
            stavka_day = stavka * ratio
    # количество дней в году
    if date.year % 4 != 0:
        year = 365
    else:
        year = 366
    subsidies_day = dolg * stavka_day / 100 / year
    # субсидии за отчетный месяц
    if date.year == fatherly_year and date.month == fatherly_month:
        subsidies_month += subsidies_day
    # субсидии за месяц, следующий за отчетным
    if date.year == fatherly_year and date.month == fatherly_month + 1:
        subsidies_next_month += subsidies_day
    # субсидии за отчетный год
    if (date.year == fatherly_year and date.month != 12) or (date.year == fatherly_year - 1 and date.month == 12):
        subsidies_year += subsidies_day
    # субсидии за год, следующий за отчетным
    if (date.year == fatherly_year+1 and date.month != 12) or (date.year == fatherly_year and date.month == 12):
        subsidies_next_year += subsidies_day
    subsidies += subsidies_day
    print(date, ', субсидии за день -', subsidies_day, ', ключевая ставка -', stavka_day)
    date += dt.timedelta(1)
print('Субсидии за всё время', subsidies)
print('Субсидии за отчетный год', subsidies_year)
print('Субсидии за отчетный месяц', subsidies_month)
print('Субсидии за за месяц, следующий за отчетным', subsidies_next_month)
print('Субсидии за за год, следующий за отчетным {}'.format(subsidies_next_year))
