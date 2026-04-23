from nicegui import ui

# --- MASTER DATA ---
orders = [
    {
        'id': 1,
        'customer': 'Alice',
        'total': 120,
        'items': [
            {'product': 'Apple', 'qty': 2},
            {'product': 'Banana', 'qty': 5},
        ],
    },
    {
        'id': 2,
        'customer': 'Bob',
        'total': 80,
        'items': [
            {'product': 'Orange', 'qty': 3},
        ],
    },
{
        'id': 3,
        'customer': 'Bob',
        'total': 80,
        'items': [
            {'product': 'Orange', 'qty': 3},
        ],
    },
{
        'id': 4,
        'customer': 'Bob',
        'total': 80,
        'items': [
            {'product': 'Orange', 'qty': 3},
        ],
    },
{
        'id': 5,
        'customer': 'Bob',
        'total': 80,
        'items': [
        ],
    },
]

# --- DETAIL GRID (пустой сначала) ---
with ui.row().classes('w-full no-wrap'):
    master_grid = ui.aggrid({
        'columnDefs': [
            {'field': 'id'},
            {'field': 'customer'},
            {'field': 'total'},
        ],
        'rowData': orders,
        'rowSelection': 'single',
        'domLayout': 'autoHeight',
    }).classes('w-3/4 min-w-0')
    detail_grid = ui.aggrid({
        'columnDefs': [
            {'field': 'product', 'headerName': 'Product'},
            {'field': 'qty', 'headerName': 'Qty'},
        ],
        'rowData': [],
        'domLayout': 'autoHeight',
    }).classes('w-1/4 min-w-0')

# ('flex-1') - по горизонтали, 'w-2/3' разная ширина

def on_row_click(e):
    row = e.args['data']
    items = row['items']

    # обновляем detail grid
    detail_grid.options['rowData'] = items
    detail_grid.update()


master_grid.on('rowClicked', on_row_click, ['data'])


ui.label('Orders').classes('text-xl')
master_grid

ui.label('Order details').classes('text-xl mt-4')
detail_grid

ui.run()