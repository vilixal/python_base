from nicegui import ui

# Список полей
fields = ['id', 'bank_name', 'tags', 'status', 'modules', 'contacts', 'app_version', 'db_version']
input_fields = [f for f in fields if f != 'id']

# Чтение русских названий из вашего словаря
COLUMN_NAME = {
    'id': 'ИД',
    'bank_name': 'Наименование банка',
    'tags': 'Тэги',
    'status': 'Статус',
    'modules': 'Модули',
    'contacts': 'Контакты',
    'app_version': 'Версия приложения',
    'db_version': 'Версия БД',
    'banklist_id': 'ИД Банка',
    'server_name': 'Имя сервера'
}

# Данные для таблицы
table_data = []


# Создаём форму
def create_form():
    inputs = {}

    with ui.card().classes('w-full'):
        ui.label('✏️ Добавление новой записи').classes('text-h6 mb-4')

        # Две колонки для компактности
        with ui.row().classes('w-full gap-4'):
            # Первая колонка
            with ui.column().classes('flex-1 gap-3'):
                for field in input_fields[:4]:  # Первые 4 поля
                    label = COLUMN_NAME.get(field, field.replace('_', ' ').title())
                    inputs[field] = ui.input(label=label).classes('w-full')

            # Вторая колонка
            with ui.column().classes('flex-1 gap-3'):
                for field in input_fields[4:]:  # Остальные поля
                    label = COLUMN_NAME.get(field, field.replace('_', ' ').title())
                    inputs[field] = ui.input(label=label).classes('w-full')

        return inputs


# Валидация
def validate_form(inputs):
    errors = []
    for field, input_widget in inputs.items():
        if field == 'bank_name' and not input_widget.value:
            errors.append('Наименование банка обязательно')
        if field == 'status' and not input_widget.value:
            errors.append('Статус обязателен')

    return errors


# Сохранение
def save_form(inputs):
    # Валидация
    errors = validate_form(inputs)
    if errors:
        for error in errors:
            ui.notify(error, type='negative')
        return

    # Собираем данные
    new_record = {
        'id': len(table_data) + 1  # Авто-инкремент
    }

    for field in input_fields:
        new_record[field] = inputs[field].value or ''

    # Добавляем в список
    table_data.append(new_record)

    # Обновляем таблицу
    update_table()

    # Очищаем форму
    for input_widget in inputs.values():
        input_widget.value = ''

    ui.notify(f'✅ Запись добавлена (ID: {new_record["id"]})',
              type='positive', position='top')


# Обновление таблицы
def update_table():
    table_container.clear()

    with table_container:
        if table_data:
            columns = [
                {'name': f, 'label': COLUMN_NAME.get(f, f), 'field': f, 'align': 'left'}
                for f in fields
            ]

            ui.table(
                columns=columns,
                rows=table_data.copy(),  # Копия для безопасности
                row_key='id',
                pagination={'rowsPerPage': 10},
                classes='w-full'
            ).classes('shadow-lg')
        else:
            ui.label('📭 Нет данных').classes('text-gray-500 text-center w-full p-8')


# Основной интерфейс
@ui.page('/')
def main_page():
    ui.label('📊 Управление записями').classes('text-h4 mb-6')

    # Создаём форму
    inputs = create_form()

    # Кнопки
    with ui.row().classes('gap-4 mt-4 mb-6'):
        ui.button('💾 Сохранить', on_click=lambda: save_form(inputs),
                  icon='save', color='primary')
        ui.button('🗑️ Очистить', on_click=lambda: [setattr(inp, 'value', '') for inp in inputs.values()],
                  icon='clear', color='grey')

    # Заголовок таблицы
    ui.label('📋 Список записей').classes('text-h6 mt-6 mb-2')

    # Контейнер для таблицы
    global table_container
    table_container = ui.column().classes('w-full')

    # Инициализация таблицы
    update_table()


ui.run(reload=False)