import re
from datetime import datetime,time

line = ('''      0 ms
''')
line2 = '2025-03-14T14:06:15.9800 (74032:0x7f313b9b9e40#1) EXECUTE_STATEMENT_FINISH'
match_timestamp = re.search(r'\s+(?P<time_execute>\d+)\sms\s', line)
print(match_timestamp)
