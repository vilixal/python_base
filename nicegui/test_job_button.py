from nicegui import ui

row_data = [
    {'name': 'ГПБ', 'status': 'Саппорт', 'id': 1},
    {'name': 'Совкомбанк', 'status': 'Отказался', 'id': 2},
]

ButtonsRenderer = """
class ButtonsRenderer {
    init(params) {
        this.eGui = document.createElement('div');
        this.eGui.style.display = 'flex';
        this.eGui.style.gap = '4px';
        this.eGui.style.alignItems = 'center';

        const editBtn = document.createElement('span');
        editBtn.innerHTML = '✏️';
        editBtn.style.cssText = `
            cursor: pointer;
            font-size: 14px;
            padding: 2px 4px;
            border-radius: 3px;
        `;

        const deleteBtn = document.createElement('span');
        deleteBtn.innerHTML = '🗑️';
        deleteBtn.style.cssText = `
            cursor: pointer;
            font-size: 14px;
            padding: 2px 4px;
            border-radius: 3px;
        `;

        editBtn.onclick = () => nicegui.emit('edit_row', params.data);
        deleteBtn.onclick = () => nicegui.emit('delete_row', params.data);

        this.eGui.appendChild(editBtn);
        this.eGui.appendChild(deleteBtn);
    }
    getGui() { return this.eGui; }
}
"""

grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name', 'headerName': 'Название банка'},
        {'field': 'status', 'headerName': 'Статус'},
        {
            'headerName': '',
            ':cellRenderer': ButtonsRenderer,
            'width': 10,
        },
    ],
    'rowData': row_data,
}).classes('w-full h-[400px]')


# Обработка событий через .on()
def handle_edit(e):
    ui.notify(f'Редактируем: {e.args["name"]}', type='info')


def handle_delete(e):
    ui.notify(f'Удаляем: {e.args["name"]}', type='warning')
    # Обновляем данные
    new_data = [row for row in row_data if row['id'] != e.args['id']]
    grid.options['rowData'] = new_data
    grid.update()


grid.on('edit_row', handle_edit)
grid.on('delete_row', handle_delete)

ui.run()