from nicegui import ui


@ui.page('/{type}')
def icons(type: str, amount: int = 1):
    with ui.column():
        ui.label(type)
        ui.input(label='ID', placeholder='start typing', value=amount)
        ui.input(label='NAME', placeholder='start typing', value='GBP')
        ui.input(label='STATUS', placeholder='start typing', value='Active')

amount=4

@ui.page('/')
def page():
    ui.link('Star', f'/star?amount={amount}')

ui.run()