from nicegui import ui

TagRenderer = """
class TagRenderer {
    init(params) {
        this.eGui = document.createElement('div');
        this.refresh(params);
    }
    refresh(params) {
        // Очищаем контейнер
        this.eGui.innerHTML = '';

        // Получаем значение ячейки (может быть строка или массив)
        let tags = params.value;
        if (typeof tags === 'string') {
            tags = tags.split(',').map(t => t.trim());
        }

        // Для каждого слова создаем стилизованный тег
        if (Array.isArray(tags)) {
            tags.forEach(tag => {
                const span = document.createElement('span');
                span.innerText = tag;
                span.style.padding = '0px 8px';
                span.style.margin = '2px';
                span.style.borderRadius = '4px';
                span.style.fontSize = '12px';
                span.style.display = 'inline-block';
                span.style.lineHeight = '1.5';

                // Назначаем цвет в зависимости от текста
                if (tag === 'ГИС ГМП') {
                    span.style.backgroundColor = '#ff4444';
                    span.style.color = 'white';
                } else if (tag === 'ФССП') {
                    span.style.backgroundColor = '#4444ff';
                    span.style.color = 'white';
                } else {
                    span.style.backgroundColor = '#cccccc';
                    span.style.color = 'black';
                }

                this.eGui.appendChild(span);
            });
        }
        return true;
    }
    getGui() {
        return this.eGui;
    }
}
"""

master_data = [
    {'name': 'ГПБ', 'status': 'Саппорт', 'module': ['ГИС ГМП', 'ФССП'], 'tag': 'Газпромбанк sas'},
    {'name': 'Совкомбанк', 'status': 'Отказался', 'module': ['ГИС ГМП', 'ФНС', 'ФССП'], 'tag': 'Совок asd'},
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

# поиск
search_input = ui.input(placeholder='Поиск').props('rounded outlined dense').props('clearable')


def apply_quick_filter():
    filter_text = search_input.value
    print(f"Фильтр: '{filter_text}'")  # Для отладки
    # Получаем текст из поля ввода
    # Всё что api.method в aggrid вызывается так
    master_grid.run_grid_method('setGridOption', 'quickFilterText', filter_text)


search_input.on_value_change(apply_quick_filter)

# мастер таблица
master_grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name', 'headerName': 'Название банка'},
        {'headerName': 'Тэг', 'field': 'tag', 'hide': True},
        {'field': 'status', 'headerName': 'Статус'},
        {
            'field': 'module',
            'headerName': 'Модули',
            ':cellRenderer': TagRenderer,  # 👈 Ключевой момент: двоеточие перед именем параметра
        }
    ],
    'rowData': master_data,
    #'autoSizeStrategy': # подбор ширины под текст ячеек
    #    {'type': 'fitCellContents'},
    'includeHiddenColumnsInQuickFilter': 'toInclude', # быстрый фильтр по скрытым полям
    'cacheQuickFilter': True, #фильтр в кэше
    'enableCellTextSelection': True, #разрешить выделять значения
    'rowHeight': 25,           # Высота строк данных
    'headerHeight': 20
}).classes('w-full h-[300px]')

detail_grid = ui.aggrid({
    'columnDefs': [
        {'field': 'server', 'headerName': 'Сервер'},
        {'field': 'status', 'headerName': 'Статус'},
    ],# 'autoSizeStrategy':
      #  {'type': 'fitCellContents'},
    'includeHiddenColumnsInQuickFilter': 'toInclude',
    'cacheQuickFilter': True,
    'enableCellTextSelection': True,
    'rowData': [],
}).classes('w-full h-[200px]')


def show_details(e):
    print("Событие сработало!")
    if e.args and 'data' in e.args:
        bank_name = e.args['data']['name']
        details = detail_data.get(bank_name, [])
        detail_grid.options['rowData'] = details
        detail_grid.update()
        n = ui.notification(timeout=3, type='negative')
        n.message = f"Показаны серверы для {bank_name}"


# Используем cellClicked
master_grid.on('rowClicked', show_details, ['data'])


def update():
    master_grid.update()


ui.button('Обновить', on_click=update)

ui.run(title='Тестовая таблица')
