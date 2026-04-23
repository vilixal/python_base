from nicegui import ui

# Определяем JavaScript класс для рендеринга цветных прямоугольников
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
                if (tag === 'Большой') {
                    span.style.backgroundColor = '#ff4444';
                    span.style.color = 'white';
                } else if (tag === 'Длинный') {
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

# Создаем таблицу
grid = ui.aggrid({
    'columnDefs': [
        {'field': 'name', 'headerName': 'Имя'},
        {
            'field': 'tags',
            'headerName': 'Теги',
            ':cellRenderer': TagRenderer,  # 👈 Ключевой момент: двоеточие перед именем параметра
        },
    ],
    'rowData': [
        {'name': 'Alice', 'tags': ['Большой', 'Длинный']},
        {'name': 'Bob', 'tags': ['Маленький', 'Короткий']},
        {'name': 'Carol', 'tags': 'Большой, Средний'},  # Можно и строкой
    ],
'rowHeight': 30
}).classes('max-h-400')

def show_details(e):
    n = ui.notification(timeout=3,type='negative')
    n.message = f'Событие сработало!{e}'
    print(f'Событие сработало!{e}')

grid.on('cellClicked', show_details, ['data'])

ui.run()