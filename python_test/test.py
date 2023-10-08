import re

email = '@1.2'
pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
if re.match(pattern,email):
    print('correct')
else:
    print('NOT')