from nicegui import ui
import json

banklist_columns_not_id=['id', 'bank_name', 'tags', 'status', 'modules', 'contacts', 'app_version', 'db_version']
COLUMN_NAME={'id':'ИД', 'bank_name':'Наименование банка', 'tags':'Тэги', 'status':'Статус', 'modules':'Модули', 'contacts':'Контакты', 'app_version':'Версия приложения', 'db_version':'Версия БД', 'banklist_id':'ИД Банка'
             , 'server_name':'Имя сервера', 'module':'Модуль', 'integration':'Интеграция', 'type':'Тип интеграции', 'comment':'Комментарий'}

master_data = [
    {'name': 'ГПБ', 'status': 'Саппорт'},
    {'name': 'Совкомбанк', 'status': 'Отказался'},
]

detail_data = {
    'ГПБ': [
        {'server': 'app1', 'status': 'Работает'},
        {'server': 'app2', 'status': 'Не работает'},
    ],
    'Совкомбанк': [
        {'server': 'app1', 'status': 'Не работает'},
    ],
}

with ui.row().classes('w-full h-[calc(100vh-32px)]'):
    with ui.column().classes('w-full flex-1'):
        with ui.card().classes('w-full'):
            for column in banklist_columns_not_id:
                if column == 'status':
                    ui.select(['Сопровождение', 'Внедрение', 'Отказался'], value='Сопровождение',
                                               label=COLUMN_NAME[column]).props('outlined')
                else:
                    ui.input(COLUMN_NAME[column]).props('outlined').classes('w-full')
            ui.button('Добавить')
    with ui.column().classes('w-full flex-1'):
        with ui.card().classes('w-full'):
            master_grid = ui.aggrid({
                'columnDefs': [
                    {'field': 'name', 'headerName': 'Название банка',
                'editable' : True},
                    {'field': 'status', 'headerName': 'Статус',
                'editable' : True},
                ],
                'rowData': master_data,
                'editType': 'fullRow'
            }).classes('w-full h-[300px]')
            ui.button('Добавить')
            with ui.element('q-fab').props('icon=navigation color=green'):
                ui.button('Сохранить 1')
                ui.button('Сохранить 2')
            with ui.card().classes('w-full'):
                ui.label('➕ Добавить банк').classes('text-h6')
                inputs = {}
                with ui.row().classes('w-full items-center gap-4'):
                    for column in banklist_columns_not_id:
                        if column == 'status':
                            ui.select(['Сопровождение', 'Внедрение', 'Отказался'],
                                                       value='Сопровождение', label=COLUMN_NAME[column]).props(
                                'outlined')
                        else:
                            ui.input(COLUMN_NAME[column]).props('outlined')
                    ui.button('Сохранить')

        with ui.card().classes('w-full'):
            detail_grid = ui.aggrid({
                'columnDefs': [
                    {'field': 'server', 'headerName': 'Сервер'},
                    {'field': 'status', 'headerName': 'Статус'},
                ],
                'rowData': [],
            }).classes('w-full h-[200px]')
            ui.button('Добавить')


ui.run()