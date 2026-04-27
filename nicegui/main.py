import database
import sys
from nicegui import events, app, ui
import asyncio

COLUMN_NAME={'id':'ИД', 'bank_name':'Наименование банка', 'tags':'Тэги', 'status':'Статус', 'modules':'Модули', 'contacts':'Контакты', 'app_version':'Версия приложения', 'db_version':'Версия БД', 'banklist_id':'ИД Банка'
             , 'server_name':'Имя сервера', 'module':'Модуль', 'integration':'Интеграция', 'type':'Тип интеграции', 'comment':'Комментарий'}
COLUMN_HIDE=[]#'id','tags','server_id','banklist_id']#

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
    banklist_columns = await database.get_columns('banklist')
    banklist_columns_not_id = banklist_columns.copy()
    banklist_columns_not_id.remove('id')
    bank_field_agg = [
        {'field': field, 'headerName': COLUMN_NAME.get(field, field),'hide': True if field in COLUMN_HIDE else False}
        for field in banklist_columns
    ]

    module_columns = await database.get_columns('module')
    module_columns_not_id = module_columns.copy()
    module_columns_not_id.remove('id')
    module_field_agg = [{'field': 'bank_name', 'headerName': COLUMN_NAME.get('bank_name', 'bank_name')}]
    module_field_agg.extend([
        {'field': field, 'headerName': COLUMN_NAME.get(field, field),'hide': True if field in COLUMN_HIDE else False}
        for field in module_columns
    ])

    server_columns = await database.get_columns('server')
    server_columns_not_id = server_columns.copy()
    server_columns_not_id.remove('id')
    server_field_agg = [
        {'field': field, 'headerName': COLUMN_NAME.get(field, field),'hide': True if field in COLUMN_HIDE else False}
        for field in server_columns
    ]


    def apply_quick_filter():
        filter_text = search_input.value
        print(f"Фильтр: '{filter_text}'")  # Для отладки
        # Получаем текст из поля ввода
        # Всё что api.method в aggrid вызывается так
        master_grid.run_grid_method('setGridOption', 'quickFilterText', filter_text)

    async def update_data():
        rows = await database.get_data('banklist')
        master_grid.options['rowData'] = [dict(row) for row in rows]
        master_grid.update()
        server_grid.update()
        module_grid.update()

    async def add_bank():
        print(list(inputs[x].value for x in banklist_columns_not_id))
        if not inputs['bank_name']:
            ui.notify('Введите название банка', type='warning')
            return
        banklist_insert_list={}
        for column in banklist_columns_not_id:
            banklist_insert_list.update({column: inputs[column].value})
        await database.add_data('banklist', banklist_insert_list)
        ui.notify(f'Банк "{inputs['bank_name'].value}" добавлен', type='positive')
        # Очищаем поля
        for column in banklist_columns_not_id:
            inputs[column].value=''
        # Обновляем таблицу
        await update_data()


    async def show_details(data):
        print(f"Выбрали запись {data}")
        if data.args and 'data' in data.args:
            bank_id = data.args['data']['id']
            bank_name = data.args['data']['bank_name']
            #server
            server_rows = await database.get_data('server',{'banklist_id':bank_id})
            server_grid.options['rowData']=[dict(row)|{'bank_name': bank_name} for row in server_rows]
            print(server_grid.options['rowData'])
            server_grid.update()
            print(f"Показаны серверы для {bank_name}")
            #module
            module_rows = await database.get_data('module',{'banklist_id':bank_id})
            module_grid.options['rowData']=[dict(row)|{'bank_name': bank_name} for row in module_rows]
            print(module_grid.options['rowData'])
            module_grid.update()
            print(f"Показаны модули для {bank_name}")




    # определение контейнеров и высоты страницы nextval('banklist_id_seq'::regclass) nextval('module_id_seq'::regclass)
    # ui.context.client.page_container.default_slot.children[0].props(
    #     ':style-fn="(offset, height) => ({ height: `calc(100vh - ${offset}px)` })"'
    # )
    # ui.context.client.content.classes("h-full")


    with ui.column().classes('w-full h-[calc(100vh-32px)]'):
        with ui.row().classes('w-full'):
            search_input = ui.input(placeholder='Поиск').props('rounded outlined dense').props('clearable').classes('w-[400px]')
            with ui.button(icon='menu').classes('ml-auto'):
                with ui.menu() as menu:
                    ui.menu_item('Пункт меню 1', lambda: result.set_text('Выбран элемент 1'))
                    ui.menu_item('Пункт меню 2', lambda: result.set_text('Выбран элемент 2'))
                    ui.menu_item('Пункт меню 3 (держать открытым)',
                                 lambda: result.set_text('Выбран элемент 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Закрыть', menu.close)


        search_input.on_value_change(apply_quick_filter)

        master_grid = ui.aggrid({
            'columnDefs': bank_field_agg,
            'rowData': [],
            # 'autoSizeStrategy': # подбор ширины под текст ячеек
            #    {'type': 'fitCellContents'},
            'includeHiddenColumnsInQuickFilter': 'toInclude',  # быстрый фильтр по скрытым полям
            'cacheQuickFilter': True,  # фильтр в кэше
            'enableCellTextSelection': True,  # разрешить выделять значения
            'rowHeight': 20,  # Высота строк данных
            'headerHeight': 20
        }).classes('w-full flex-1/2').on('rowClicked', show_details, ['data'])

        with ui.row().classes('w-full flex-1'):
            server_grid = ui.aggrid({
                'columnDefs': server_field_agg,
                'rowData': [],
                # 'autoSizeStrategy': # подбор ширины под текст ячеек
                #    {'type': 'fitCellContents'},
                'includeHiddenColumnsInQuickFilter': 'toInclude',  # быстрый фильтр по скрытым полям
                'cacheQuickFilter': True,  # фильтр в кэше
                'enableCellTextSelection': True,  # разрешить выделять значения
                'rowHeight': 20,  # Высота строк данных
                'headerHeight': 20
            }).classes('w-full flex-1')


            module_grid = ui.aggrid({
                'columnDefs': module_field_agg,
                'rowData': [],
                # 'autoSizeStrategy': # подбор ширины под текст ячеек
                #    {'type': 'fitCellContents'},
                'includeHiddenColumnsInQuickFilter': 'toInclude',  # быстрый фильтр по скрытым полям
                'cacheQuickFilter': True,  # фильтр в кэше
                'enableCellTextSelection': True,  # разрешить выделять значения
                'rowHeight': 20,  # Высота строк данных
                'headerHeight': 20
            }).classes('w-full flex-1')


        data = {'show_card': False}
        ui.switch('Показать карточку', value=False).bind_value_to(data, 'show_card')
        with ui.card().classes('w-full').bind_visibility_from(data, 'show_card'):
            ui.label('➕ Добавить банк').classes('text-h6')
            inputs = {}
            with ui.row().classes('w-full items-center gap-4'):
                for column in banklist_columns_not_id:
                    if column == 'status':
                        inputs[column] = ui.select(['Сопровождение', 'Внедрение', 'Отказался'],value='Сопровождение',label=COLUMN_NAME[column]).props('outlined')
                    else:
                        inputs[column] = ui.input(COLUMN_NAME[column]).props('outlined')
                ui.button('Добавить', on_click=add_bank, icon='add').props('color=primary')

    # Загружаем данные при открытии страницы
    await update_data()


# ============================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ============================================
if __name__ in {"__main__", "__mp_main__"}:
    try:
        ui.run(reload=True)
    except KeyboardInterrupt:
        # Игнорируем KeyboardInterrupt
        print("\nПриложение остановлено пользователем")
        sys.exit(0)
    except Exception as e:
        # Другие ошибки логируем
        print(f"Ошибка: {e}")
        sys.exit(1)
