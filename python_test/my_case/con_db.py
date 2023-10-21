from datetime import timedelta, datetime

import fdb

con = fdb.connect(dsn='127.0.0.1:e:/id-sys2/db/cirim.fdb', user='SYSDBA', password='masterkey')

# Объект курсора
cur = con.cursor()

# Выполняем запрос
dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
cur.execute("select * from TEST")

# cur.fetchall() возвращает список из кортежей. Адресуемся к единственному значению; + перевод строки
print(str(cur.fetchall()))