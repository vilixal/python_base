from nicegui import ui
import json

bank_name='UG<'
where={'banklist_id':2}
row=dict(where).append('bank_name':bank_name)
print(row)