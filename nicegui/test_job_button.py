from nicegui import ui
from nicegui.events import ValueChangeEventArguments

size_value=20

def update_table():
    grid.options['rowHeight']=size_value
    grid.update()


slider = ui.slider(min=15, max=50, value=size_value)
slider.bind_value(globals(), 'size_value')
slider.on('update:model-value', lambda event: update_table())
ui.label().bind_text_from(globals(), 'size_value', lambda v: f'Значение: {v}')

row_data = [
    {'name': 'ГПБ', 'status': 'Саппорт', 'id': 1},
    {'name': 'Совкомбанк', 'status': 'Отказался', 'id': 2},
]

ButtonsRenderer = f"""
class ButtonsRenderer {{
    init(params) {{
        this.eGui = document.createElement('div');
        this.eGui.style.display = 'flex';
        this.eGui.style.gap = '4px';
        this.eGui.style.alignItems = 'center';

        const editBtn = document.createElement('span');
        editBtn.innerHTML = '✏️';
        editBtn.style.cssText = `
            cursor: pointer;
            font-size: {size_value*0.6}px;
            width: {size_value*0.8}px;
            height: {size_value*0.8}px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            background: white;
            transition: all 0.2s ease;
            margin: 1px 2px;
            opacity: 0.7;
        `;
        
        editBtn.onmouseenter = () => {{
            editBtn.style.backgroundColor = '#f8fafc';
            editBtn.style.borderColor = '#3b82f6';
            editBtn.style.opacity = '1';
            editBtn.style.transform = 'scale(1.05)';
        }};
        
        editBtn.onmouseleave = () => {{
            editBtn.style.backgroundColor = 'white';
            editBtn.style.borderColor = '#e2e8f0';
            editBtn.style.opacity = '0.7';
            editBtn.style.transform = 'scale(1)';
        }};

        const deleteBtn = document.createElement('span');
        deleteBtn.innerHTML = '❌';
        deleteBtn.style.cssText = `
        cursor: pointer;
            font-size: {size_value*0.6}px;
            width: {size_value*0.8}px;
            height: {size_value*0.8}px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        background: white;
        transition: all 0.2s ease;
        margin: 1px 2px;
        opacity: 0.7;
      `;

        deleteBtn.onmouseenter = () => {{
            deleteBtn.style.backgroundColor = '#f8fafc';
            deleteBtn.style.borderColor = '#3b82f6';
            deleteBtn.style.opacity = '1';
            deleteBtn.style.transform = 'scale(1.05)';
        }};
        
        deleteBtn.onmouseleave = () => {{
            deleteBtn.style.backgroundColor = 'white';
            deleteBtn.style.borderColor = '#e2e8f0';
            deleteBtn.style.opacity = '0.7';
            deleteBtn.style.transform = 'scale(1)';
        }};

        editBtn.onclick = () => nicegui.emit('edit_row', params.data);
        deleteBtn.onclick = () => nicegui.emit('delete_row', params.data);

        this.eGui.appendChild(editBtn);
        this.eGui.appendChild(deleteBtn);
    }}
    getGui() {{ return this.eGui; }}
}}
"""

grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name', 'headerName': 'Название банка'},
        {'field': 'status', 'headerName': 'Статус'},
        {'field': 'button',
            'headerName': '',
            ':cellRenderer': ButtonsRenderer,
         'width': 20,
         'minWidth': 20,

        },
    ],
    'rowData': row_data,
    'rowHeight': size_value,  # Высота строк данных
    'headerHeight': size_value
}).classes('w-full h-[400px]')
# grid.run_grid_method('autoSizeColumns', ['button'])
# grid.run_grid_method('sizeColumnsToFit')



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