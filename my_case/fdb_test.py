import fdb
from pprint import pprint

query='''select cast(d.create_date as date), d.docstatus_caption, count(*)
from DOCUMENT D
where d.documentclassid = 450
and d.create_date > dateadd(day, -200, current_date) -- отобраны запросы СПИ за неделю
group by 1, 2'''


con = fdb.connect(dsn='192.168.1.222:ncore-bank', user='SYSDBA', password='masterkey')
cursor = con.cursor()
cursor.execute(query)
row = cursor.fetchall()
pprint(row)