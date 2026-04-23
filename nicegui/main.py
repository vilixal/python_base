import database
import sys
from nicegui import app, ui

COLUMN_NAME={'id':'ИД', 'bank_name':'Наименование банка', 'tags':'Тэги', 'status':'Статус', 'modules':'Модули', 'contacts':'Контакты', 'app_version':'Версия приложения', 'db_version':'Версия БД', 'banklist_id':'ИД Банка'
             , 'server_name':'Имя сервера'}

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


@ui.page('/')
async def main_page():
    columns = await database.get_columns('banklist')
    bank_columns = [
        {'field': field, 'headerName': COLUMN_NAME.get(field, field)}
        for field in columns
    ]

    search_input = ui.input(placeholder='Поиск').props('rounded outlined dense').props('clearable')

    def apply_quick_filter():
        filter_text = search_input.value
        print(f"Фильтр: '{filter_text}'")  # Для отладки
        # Получаем текст из поля ввода
        # Всё что api.method в aggrid вызывается так
        master_grid.run_grid_method('setGridOption', 'quickFilterText', filter_text)

    search_input.on_value_change(apply_quick_filter)

    master_grid = ui.aggrid({
        'columnDefs': bank_columns,
        'rowData': [],
        # 'autoSizeStrategy': # подбор ширины под текст ячеек
        #    {'type': 'fitCellContents'},
        'includeHiddenColumnsInQuickFilter': 'toInclude',  # быстрый фильтр по скрытым полям
        'cacheQuickFilter': True,  # фильтр в кэше
        'enableCellTextSelection': True,  # разрешить выделять значения
        'rowHeight': 25,  # Высота строк данных
        'headerHeight': 20
    }).classes('w-full h-[300px]')

    async def update_data():
        rows = await database.get_data('banklist')
        master_grid.options['rowData'] = [dict(row) for row in rows]
        master_grid.update()
    #
    #
    # async def add_bank():
    #     name = name_input.value
    #     status = status_select.value
    #     version = version_input.value or '1.9.100.0'
    #
    #     if not name:
    #         ui.notify('Введите название банка', type='warning')
    #         return
    #
    #     async with database.DB_POOL.acquire() as conn:
    #         await conn.execute("""
    #                            INSERT INTO banklist (bank_name, status, app_version)
    #                            VALUES ($1, $2, $3)
    #                            """, name, status, version)
    #
    #     # Очищаем поля
    #     name_input.value = ''
    #     version_input.value = ''
    #     ui.notify(f'Банк "{name}" добавлен', type='positive')
    #
    #     # Обновляем таблицу
    #     await load_data()

    with ui.card().classes('q-mb-md w-full'):
        ui.label('➕ Добавить банк').classes('text-h6')

        with ui.row().classes('w-full items-center gap-4'):
            name_input = ui.input('Название банка').props('outlined')
            status_select = ui.select(
                ['active', 'inactive'],
                value='active',
                label='Статус'
            ).props('outlined')
            version_input = ui.input('Версия', placeholder='1.0.0').props('outlined')
            ui.button('Добавить')#, on_click=add_bank, icon='add').props('color=primary')

    # Загружаем данные при открытии страницы
    await update_data()


# ============================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ============================================
if __name__ in {"__main__", "__mp_main__"}:
    try:
        ui.run(reload=False)
    except KeyboardInterrupt:
        # Игнорируем KeyboardInterrupt
        print("\nПриложение остановлено пользователем")
        sys.exit(0)
    except Exception as e:
        # Другие ошибки логируем
        print(f"Ошибка: {e}")
        sys.exit(1)
