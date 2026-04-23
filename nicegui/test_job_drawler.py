from nicegui import ui

# --- DATA ---
rows = [
    {'id': 1, 'name': 'Alice', 'age': 25, 'city': 'London'},
    {'id': 2, 'name': 'Bob', 'age': 30, 'city': 'New York'},
]

# --- DETAIL UI ---
drawer = ui.right_drawer().classes('bg-white w-80')

with drawer:
    detail_column = ui.column().classes('p-4')


# --- HANDLER ---
def show_details(e):
    row = e.args['data']

    detail_column.clear()

    with detail_column:
        ui.label(f"User: {row['name']}").classes('text-xl')
        ui.label(f"Age: {row['age']}")
        ui.label(f"City: {row['city']}")

    drawer.clear()

# --- GRID ---
grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name'},
        {'field': 'age'},
        {'field': 'city'},
    ],
    'rowData': rows,
}).on('rowClicked', show_details, ['data']).classes('w-full h-64')

ui.label('Users').classes('text-xl')

ui.run()