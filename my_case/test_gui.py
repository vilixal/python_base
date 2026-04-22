from nicegui import ui

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
'autoSizeStrategy': {
        'type': 'fitCellContents'}
}).classes('h-[400px]')

ui.run()