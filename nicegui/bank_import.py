import pandas as pd
import numpy as np
import database



COLUMN_LINK = {'bank_name': 'Клиент', 'module_name': 'Модуль', 'status': 'Статус сопровождения',
               'contacts': 'Контакт для рассылки', 'app_version': 'Версия',
               'integration': 'Технологии интеграции', 'type': 'Описание интеграции', 'comment': 'Комментарий',}


async def load_data_file():
    df = pd.read_excel('bank.xlsx')
    df = df.replace({np.nan: None})
    grouped = df.groupby('Клиент')
    banklist_columns = await database.get_columns('banklist')
    banklist_columns_not_id = banklist_columns.copy()
    banklist_columns_not_id.remove('id')
    module_columns = await database.get_columns('module')
    module_columns_not_id = module_columns.copy()
    module_columns_not_id.remove('id')
    server_columns = await database.get_columns('server')
    server_columns_not_id = server_columns.copy()
    server_columns_not_id.remove('id')
    bank_id=0
    for name, group in grouped:
        status='Не определено'
        if (group['Статус сопровождения'] == 'Стандарт').any():
            status='Стандарт'
        elif (group['Статус сопровождения'] == 'Внедрение').any():
            status = 'Внедрение'
        elif (group['Статус сопровождения'] == 'Приостановлено').any():
            status = 'Приостановлено'
        elif (group['Статус сопровождения'] == 'Отказался').any():
            status = 'Отказался'
        elif (group['Статус сопровождения'] == 'Отозвана лицензия').any():
            status = 'Отозвана лицензия'
        bank_dict_insert = {}
        for column in banklist_columns_not_id:
            if column == 'bank_name':
                bank_dict_insert[column]=name
            elif column == 'status':
                bank_dict_insert[column] = status
            else:
                bank_dict_insert[column]=None

        bank_id=await database.add_data('banklist', bank_dict_insert)
        print(f'Вставлена запись в banklist {bank_id}')
        for index, row in group.iterrows():
            dict_insert={}
            if 'Ядро_Б' in row[COLUMN_LINK['module_name']]:
                table_insert='server'
                insert_columns_not_id=server_columns_not_id
            else:
                table_insert='module'
                insert_columns_not_id=module_columns_not_id
            for column in insert_columns_not_id:
                if column in COLUMN_LINK:
                    dict_insert[column]=row[COLUMN_LINK[column]]
                elif column == 'banklist_id':
                    dict_insert[column]=bank_id
                else:
                    dict_insert[column]=None
            await database.add_data(table_insert, dict_insert)
    return bank_id


# for name, group in grouped:
#     print(name, group)
# print(grouped.get_group('АО Дом РФ (VIP)'))
# print((domrf['Статус сопровождения'] == 'Стандар2').any())
# print(list_dict)
# анализируем группу банка на статус по порядку: Стандарт с обновлением, Стандарт, SLA, SLA с отчетностью, Внедрение, Приостановлено, Отказался, Отозвана лицензия, else Не определено
# в перпективе анализируем группу на максимальное значение версии и СУБД
# пишем основную запись
# пишем модули в модули, Ядро_Б пишем в сервера. Добавляем в основую запись модуль (или делаем заранее кокантенатацию
#
# апдейты делаем для интерфейса. Для повторного импорта нужно расширять логику на проверки


