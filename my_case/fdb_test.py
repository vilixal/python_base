import fdb

query='''select IP_NUM, ID_RESPONSE, DOC_NUM, ID, CORRESPONDENT_NAME, CORRESPONDENT_INN, DOC_IS_BASE, DOC_ID from V_IP_DOC_CORRESPONDENT'''


con = fdb.connect(dsn='192.168.1.222:ncore-bank', user='SYSDBA', password='masterkey')
cursor = con.cursor()
cursor.execute(query)
row = cursor.fetchall()
print(row)