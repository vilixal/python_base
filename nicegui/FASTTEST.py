from nicegui import ui

list_modules_for_label = ['ГИП_ЗН.Подписка', 'ГИС_ОО', 'ГИС.ГМП_ЗН(СМЭВ)']
ui.add_head_html('<style>.q-scrollarea__content{padding:0 !important}</style>')

with ui.card().classes('w-full p-0 pl-2'):  # убираем padding у card
    with ui.scroll_area().classes(''):  # убираем padding у scroll_area
        module_list_label = ui.markdown('Список модулей:').classes('')

ui.run()