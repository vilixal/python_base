from nicegui import ui

with ui.row().classes('w-full'):
    ui.button('Кнопка 1')
    ui.label('Какой-то текст')
    ui.button('Кнопка 2').classes('ml-auto')  # уедет вправо
ui.run()