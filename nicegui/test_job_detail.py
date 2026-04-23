from nicegui import ui

rows = [
    {'id': 1, 'name': 'Alice', 'expanded': False, 'details': [
        {'product': 'Apple', 'qty': 2},
        {'product': 'Banana', 'qty': 5},
    ]},
    {'id': 2, 'name': 'Bob', 'expanded': False, 'details': [
        {'product': 'Orange', 'qty': 3},
    ]},
]


def build_rows():
    result = []
    for r in rows:
        result.append(r)
        if r['expanded']:
            result.append({
                'detail': True,
                'parent': r['id'],
                'text': f"Details for {r['name']}"
            })
    return result


def toggle(e):
    row = e.args['data']
    print(row)
    if row.get('details'):
        return

    for r in rows:
        if r['id'] == row['id']:
            r['expanded'] = not r['expanded']

    grid.options['rowData'] = build_rows()
    grid.update()


grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name'},
    ],
    'rowData': build_rows(),
}).on('rowClicked', toggle, ['data'])

ui.add_head_html("""
<style>
.ag-row.detail-row {
    overflow: hidden;
    max-height: 0;
    transition: max-height 0.3s ease;
}
.ag-row.detail-row.open {
    max-height: 100px;
}
</style>
""")

ui.run()