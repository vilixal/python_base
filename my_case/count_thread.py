import re
import pprint
from datetime import datetime

process_dict = {}
with open(r'D:\temp\pochta\совком\нг19\logs.backup.2025-02-19_1042', encoding='utf8') as file:
    for line in file:
        match = re.search(
            r'(19.02.25 10:[0-9]{2}:[0-9]{2}.[0-9]{3}),(https-jsse-nio-8443-exec-[0-9]+),INFO,Application,Application version: 1.9.26.0',
            line)
        if match:
            date_process = datetime.strptime(match.group(1), '%d.%m.%y %H:%M:%S.%f')
            if match.group(2) in process_dict:
                delta = date_process - process_dict[match.group(2)][0]
                process_dict[match.group(2)][1] += 1
                process_dict[match.group(2)][0] = date_process
                process_dict[match.group(2)][2].append(delta)
            else:
                process_dict[match.group(2)] = [date_process, 1, []]

process_count = 0

for i, keys in process_dict.items():
    max_date = max(process_dict[i][2])
    sum_date = process_dict[i][2][0] - process_dict[i][2][0]
    for date in process_dict[i][2]:
        sum_date += date
    process_dict[i][2] = str(sum_date / process_dict[i][1])
    process_dict[i][0] = str(max_date)
    process_count += process_dict[i][1]

pprint.pp(process_dict)
print(len(process_dict), process_count)
