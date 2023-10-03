import datetime as dt

date1 = dt.date(2022, 4, 10)
date2 = dt.date(2022, 4, 10)
date3 = dt.date(2023, 5, 1)
date4 = dt.date(2022, 4, 10)
date5 = dt.date(2022, 5, 1)
plan = {date1: 360, date2: 270, date3: 2345, date4: 123, date5: -123}

delta = date5 - date1
date = date1
date_list = [date]
for i in range(delta.days):
    date += dt.timedelta(1)
    date_list.append(date)
    print(date)
    print(date_list)

print(delta.days)
