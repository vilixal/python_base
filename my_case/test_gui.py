from nicegui import ui

data = {'show_card': False}

with ui.row().classes('w-full'):
    with ui.button(icon='menu').classes('items-end'):
        with ui.menu() as menu:
            ui.menu_item('Пункт меню 1', lambda: result.set_text('Выбран элемент 1'))
            ui.menu_item('Пункт меню 2', lambda: result.set_text('Выбран элемент 2'))
            ui.menu_item('Пункт меню 3 (держать открытым)',
                         lambda: result.set_text('Выбран элемент 3'), auto_close=False)
            ui.separator()
            ui.menu_item('Закрыть', menu.close)

ui.aggrid({
    'columnDefs': [
        {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
        {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
    ],
    'rowData': [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'asd', 'age': 42},
{'name': 'ыol', 'age': 42},
{'name': 'ASDol', 'age': 42},
    ],
}).classes('h-[300px]')


with ui.row().classes('w-full'):
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'asd', 'age': 42},
    {'name': 'ыol', 'age': 42},
    {'name': 'ASDol', 'age': 42},
        ],
    }).classes('h-[350px] flex-1')
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'asd', 'age': 42},
    {'name': 'ыol', 'age': 42},
    {'name': 'ASDol', 'age': 42},
        ],
    }).classes('h-[350px] flex-1')

with ui.row().classes('w-full'):
    ui.input('CHTO TO').props('outlined').classes('flex-initial')
    ui.input('CHTO TO').props('outlined').classes('flex-auto')

ui.switch('Показать карточку', value=False).bind_value_to(data, 'show_card')

with ui.card().classes('w-full').bind_visibility_from(data, 'show_card'):
    ui.label('➕ Добавить банк').classes('text-h6')
    inputs = {}
    with ui.row().classes('w-full items-center gap-4'):
        ui.input('asdasdas').props('outlined')
        ui.button('Добавить', icon='add').props('color=primary')


ui.run()