import csv
import re


def new_line():
    global timestamp, process_id, thread_id, thread_number, event, db, attachment, user, process_name, transaction, sql_text, time_execute
    timestamp, process_id, thread_id, thread_number, event, db, attachment, user, process_name, transaction, sql_text, time_execute = (
                                                                                                                                          '',) * 12


lst_trace = []
first_line_sql = False
with open(r'ncore-bank.fdb.fbtrace_text', encoding='utf8') as file:
    for line in file:
        match_timestamp = re.match(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{4})\s\((?P<process_id>\d+):(?P<thread_id>\w+)#(?P<thread_number>\d+)\)\s(?P<event>\w+)',
            line)
        if match_timestamp:
            new_line()
            timestamp = match_timestamp.group("timestamp")
            process_id = match_timestamp.group("process_id")
            thread_id = match_timestamp.group("thread_id")
            thread_number = match_timestamp.group("thread_number")
            event = match_timestamp.group("event")
            continue
        match_att = re.search(
            r'(?P<db>[-a-zA-Z0-9_]+)\s\(ATT_(?P<attachment>\d+),\s(?P<user>[-a-zA-Z0-9_]+):\w+,\s\w+,\s', line)
        if match_att:
            db = match_att.group('db')
            attachment = match_att.group('attachment')
            user = match_att.group('user')
            continue
        match_proc = re.search(r'(?P<process_name>NCORE:[-_a-zA-Zа-яА-Я\d\s\[\]().:]+):\d+$', line)
        if match_proc:
            process_name = match_proc.group('process_name')
            continue
        match_transaction = re.search(r'\(TRA_(?P<transaction>\d+),\s\w+\s\|\s\w+\s\|\s\w+\s\d+\s\|\s\w+\)$', line)
        if match_transaction:
            transaction = match_transaction.group('transaction')
            continue
        match_sql = re.search(r'[-]{79}', line)
        match_end_sql = re.search(r'[\^]{79}', line)
        if match_end_sql:
            first_line_sql = False
            continue
        if first_line_sql:
            sql_text += ' ' + line
            continue
        if match_sql:
            first_line_sql = True
            sql_text = ''
            match_sql = None
            continue
        match_execute = re.search(r'(?P<time_execute>\d+)\sms,\s\d+\s', line)
        if match_execute:
            time_execute = match_execute.group('time_execute')
            lst_trace.append(
                [timestamp, db, process_id, thread_id, thread_number, attachment, user, process_name, transaction,
                 event, time_execute, sql_text.strip()])

HEADER = ['Время', 'База данных', 'Идентификатор процесса', 'Поток', 'Номер в рамках потока', 'Attachment',
          'Пользователь', 'Имя процесса', 'Транзакция', 'Событие', 'Время выполнения в мс',
          'SQL']
with open('trace.csv', 'w', newline='', encoding='cp1251') as out_file:
    writer = csv.writer(out_file, quotechar='"', delimiter=';')
    writer.writerow(HEADER)
    for line in lst_trace:
        writer.writerow(line)
