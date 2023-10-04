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

fatherly_year = 2022
fatherly_month = 10

date = date1

subsidies_day, subsidies_month, subsidies, dolg, stavka, stavka_day, subsidies_year = 0, 0, 0, 0, 0, 0, 0
while date <= date5:
    subsidies_day, dolg, stavka_day = 0, 0, 1
    # расчет долга за день
    for date_operation, operation in plan.items():
        if date_operation < date:
            dolg += operation
    # расчет ставки за день
    for date_operation, stavka in stavka_list.items():
        if date_operation < date:
            stavka_day = stavka
    # количество дней в году
    if date.year % 4 != 0:
        year = 365
    else:
        year = 366
    subsidies_day = dolg * stavka_day / 100 / year
    # субсидии за отчетный месяц
    if date.year == fatherly_year and date.month == fatherly_month:
        subsidies_month += subsidies_day
    # субсидии за отчетный год
    if (date.year == fatherly_year and date.month != 12) or (date.year == fatherly_year-1 and date.month == 12):
        subsidies_year += subsidies_day
    subsidies += subsidies_day
    date += dt.timedelta(1)
print('Субсидии за всё время', subsidies)
print('Субсидии за отчетный год', subsidies_year)
print('Субсидии за отчетный месяц', subsidies_month)
