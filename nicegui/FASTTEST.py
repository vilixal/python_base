from nicegui import events, ui

grid = ui.aggrid({})

def handle_theme_change(e: events.ValueChangeEventArguments):
    grid.classes(add='ag-theme-balham-dark' if e.value else 'ag-theme-balham',
                 remove='ag-theme-balham ag-theme-balham-dark')

ui.switch('Dark', on_change=handle_theme_change)

ui.run()