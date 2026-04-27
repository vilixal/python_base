import pandas as pd
import xlrd

# Read the .xls file
df = pd.read_excel('bank.xlsx')
grouped = df.groupby('Клиент')
domrf=grouped.get_group('АО Дом РФ (VIP)')
domrf.get('Статус сопровождения')

for index,row in domrf.iterrows():
    print(index)
    print(row['ИД'])
list_dict=domrf.to_dict(orient='records')

# for name, group in grouped:
#     print(name, group)
# print(grouped.get_group('АО Дом РФ (VIP)'))
# print((domrf['Статус сопровождения'] == 'Стандар2').any())
# print(list_dict)
#анализируем группу банка на статус по порядку: Стандарт с обновлением, Стандарт, SLA, SLA с отчетностью, Внедрение, Приостановлено, Отказался, Отозвана лицензия, else Не определено
# в перпективе анализируем группу на максимальное значение версии и СУБД
#пишем основную запись
#пишем модули в модули, Ядро_Б пишем в сервера. Добавляем в основую запись модуль (или делаем заранее кокантенатацию
#
# апдейты делаем для интерфейса. Для повторного импорта нужно расширять логику на проверки