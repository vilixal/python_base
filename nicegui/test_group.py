from nicegui import ui

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

master_grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name', 'headerName': 'Название банка'},
        {'field': 'status', 'headerName': 'Статус'},
    ],
    'rowData': master_data,
}).classes('w-full h-[300px]')

detail_grid = ui.aggrid({
    'columnDefs': [
        {'field': 'server', 'headerName': 'Сервер'},
        {'field': 'status', 'headerName': 'Статус'},
    ],
    'rowData': [],
}).classes('w-full h-[200px]')

def show_details(e):
    print("Событие сработало!")
    if e.args and 'data' in e.args:
        bank_name = e.args['data']['name']
        details = detail_data.get(bank_name, [])
        detail_grid.options['rowData'] = details
        detail_grid.update()
        print(f"Показаны серверы для {bank_name}")

# Используем cellClicked
master_grid.on('rowClicked', show_details, ['data'])

ui.run()