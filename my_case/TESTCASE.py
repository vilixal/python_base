import re

a='NCORE:[WEB] - iDiВБанк_1_9 v1.9.33.1 (IP:10.10.10.29):-2'

match_proc = re.search(r'(?P<process_name>[-_a-zA-Zа-яА-Я\d\s\[\]().:]+):[-]?\d+$', a)
print(match_proc)