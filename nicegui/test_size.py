from nicegui import ui

search_input = ui.input('Поиск') \
    .props('clearable') \
    .classes('w-full mb-4')

ui.label().bind_text_from(search_input, 'value')

# auto_size_columns передается как параметр при создании таблицы
grid = ui.aggrid(
    {
        'columnDefs': [
            {'headerName': 'Наименование', 'field': 'name'},
            {'headerName': 'Тэг', 'field': 'tag', 'hide': True},
            {'headerName': 'Статус', 'field': 'status', 'editable': True},
        ],
        'rowData': [
            {'name': 'ГПБ', 'tag': 'Газпромбанк sas', 'status': 'Саппорт'},
            {'name': 'Совкомбанк', 'tag': 'Совок asd', 'status': 'Отказался'},
        ], 'autoSizeStrategy':
        {'type': 'fitCellContents'},
'includeHiddenColumnsInQuickFilter':'toInclude',
'cacheQuickFilter': True,
        'enableCellTextSelection': True,
#'onCellClicked': '(event: CellClickedEvent) => console.log("Cell was clicked")'

    },
    # auto_size_columns=False  # 👈 Вот как это работает

)
#grid.run_grid_method('autoSizeAllColumns')
#включить скрытые поля в поиск
#grid.run_grid_method('setGridOption','includeHiddenColumnsInQuickFilter','toInclude')
#grid.run_grid_method('setGridOption','cacheQuickFilter',True)

def update():
    grid.update()

ui.button('Обновить', on_click=update)

def apply_quick_filter():
    filter_text = search_input.value
    print(f"Фильтр: '{filter_text}'")  # Для отладки
    # Получаем текст из поля ввода
    # Всё что api.method в aggrid вызывается так
    grid.run_grid_method('setGridOption', 'quickFilterText', filter_text)

search_input.on_value_change(apply_quick_filter)

ui.run(title='Тестовая таблица')
