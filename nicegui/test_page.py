from nicegui import ui

@ui.page('/icon/{icon}')
def icons(icon: str, amount: int = 1):
    ui.label(icon).classes('text-h3')
    with ui.row():
        [ui.icon(icon).classes('text-h3') for _ in range(amount)]
ui.link('Звезда', '/icon/star?amount=5')
ui.link('Дом', '/icon/home')
ui.link('Вода', '/icon/water_drop?amount=3')

ui.run()