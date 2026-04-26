from nicegui import ui

with ui.button('Добавить', on_click=lambda: dialog.open()):
    pass

with ui.dialog() as dialog, ui.card():
    ui.label('Добавление записи')
    input1 = ui.input('Поле 1')
    input2 = ui.input('Поле 2')
    input3 = ui.input('Поле 3')

    with ui.row():
        ui.button('Сохранить', on_click=lambda: save_data(), color='green')
        ui.button('Отмена', on_click=lambda: dialog.close())


def save_data():
    ui.notify(f'Сохранено: {input1.value}, {input2.value}, {input3.value}')
    dialog.close()
    input1.value = ''
    input2.value = ''
    input3.value = ''


ui.run()