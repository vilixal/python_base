import csv
import re
from pprint import pprint

lst_trace = {}
process_name = 'TEST'
with open(r'D:\devel\PyChampProject\python_base\release\logs.txt', encoding='utf8') as file:
    for line in file:
        match_timestamp = re.match(
            r'(?P<timestamp>\d{2}.\d{2}.\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}),(?P<process_name>[^,]+),(DEBUG|ERROR|INFO|WARN),',
            line)
        if match_timestamp:
            timestamp = match_timestamp.group("timestamp")
            process_name = match_timestamp.group("process_name")
        if lst_trace.get(process_name) is None:
            lst_trace.setdefault(process_name,0)

        lst_trace[process_name] += len(line)

pprint(lst_trace)
