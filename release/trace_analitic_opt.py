import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TraceRecord:
    timestamp: str = ''
    db: str = ''
    process_id: str = ''
    thread_id: str = ''
    thread_number: str = ''
    attachment: str = ''
    user: str = ''
    process_name: str = ''
    transaction: str = ''
    event: str = ''
    time_execute: str = ''
    sql_text: str = ''


def parse_trace_file(file_path: Path) -> list[TraceRecord]:
    records = []
    current = TraceRecord()
    in_sql_block = False
    sql_lines = []

    # Компилируем регулярки один раз для производительности
    re_timestamp = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{4})\s\((?P<process_id>\d+):(?P<thread_id>\w+)(?:#(?P<thread_number>\d+))?\)\s(?P<event>[ \w]+)'
    )
    re_attachment = re.compile(
        r'(?P<db>[-a-zA-Z0-9_]+)\s\(ATT_(?P<attachment>\d+),\s(?P<user>[-a-zA-Z0-9_]+):\w+,\s\w+,\s'
    )
    re_process = re.compile(r'^\s*(?P<process_name>.+):-?\d+$')
    re_transaction = re.compile(r'\(TRA_(?P<transaction>\d+),\s\w+\s\|\s\w+\s\|\s\w+\s\d+\s\|\s\w+\)$')
    re_exec_time = re.compile(r'\s+(?P<time_execute>\d+)\sms[\s,]')
    re_sql_start = re.compile(r'[-]{79}')
    re_sql_end = re.compile(r'[\^]{79}')

    with open(file_path, encoding='utf8') as f:
        for line in f:
            # 1. Начало новой записи
            if m := re_timestamp.match(line):
                if current.event and current.event not in ('', None):  # Сохраняем предыдущую
                    records.append(current)
                current = TraceRecord(
                    timestamp=m.group('timestamp'),
                    process_id=m.group('process_id'),
                    thread_id=m.group('thread_id'),
                    thread_number=m.group('thread_number') or '',
                    event=m.group('event')
                )
                in_sql_block = False
                sql_lines = []
                continue

            if in_sql_block:
                if re_sql_end.search(line):
                    current.sql_text = ' '.join(sql_lines).strip()
                    in_sql_block = False
                    continue
                sql_lines.append(line.strip())
                continue

            if re_sql_start.search(line):
                in_sql_block = True
                sql_lines = []
                continue

            # 2. Парсим остальные поля (только если не в SQL блоке)
            if m := re_attachment.search(line):
                current.db = m.group('db')
                current.attachment = m.group('attachment')
                current.user = m.group('user')
            elif m := re_process.search(line):
                current.process_name = m.group('process_name')
            elif m := re_transaction.search(line):
                current.transaction = m.group('transaction')
            elif m := re_exec_time.search(line):
                current.time_execute = m.group('time_execute')
                records.append(current)  # Запись завершена
                current = TraceRecord()  # Сбрасываем для следующей

    return records


def save_to_csv(records: list[TraceRecord], output_path: Path):
    header = ['Время', 'База данных', 'Идентификатор процесса', 'Поток', 'Номер в рамках потока',
              'Attachment', 'Пользователь', 'Имя процесса', 'Транзакция', 'Событие',
              'Время выполнения в мс', 'SQL']

    with open(output_path, 'w', newline='', encoding='cp1251') as f:
        writer = csv.writer(f, quotechar='"', delimiter=';')
        writer.writerow(header)
        for r in records:
            writer.writerow([
                r.timestamp, r.db, r.process_id, r.thread_id, r.thread_number,
                r.attachment, r.user, r.process_name, r.transaction, r.event,
                r.time_execute, r.sql_text
            ])


def main():
    input_file = Path(r'D:\devel\PyCharmProject\python_base\release\trace.txt')
    output_file = Path('trace1.csv')

    if not input_file.exists():
        print(f'Ошибка: файл {input_file} не найден')
        return

    print('Парсинг файла...')
    records = parse_trace_file(input_file)
    print(f'Найдено записей: {len(records)}')

    save_to_csv(records, output_file)
    print(f'Результат сохранён в {output_file}')


main()