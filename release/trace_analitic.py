import csv
import re
import sys
from datetime import datetime
from pathlib import Path


def find_files(directory: Path):
    """Ищет файлы .txt и .fbtrace_text в каталоге (без рекурсии)."""
    files = []
    for pattern in ("*.txt", "*.fbtrace_text"):
        files.extend(directory.glob(pattern))
    # Сортируем по имени для предсказуемого порядка
    return sorted(set(files))


def choose_file(files):
    """Даёт пользователю выбрать файл или возвращает единственный."""
    if not files:
        print("В каталоге нет файлов .txt или .fbtrace_text")
        sys.exit(1)

    if len(files) == 1:
        print(f"Найден один файл: {files[0].name}")
        return files[0]

    # Несколько файлов — предлагаем выбор
    print("Найдено несколько файлов:")
    for i, f in enumerate(files, start=1):
        print(f"  {i}. {f.name}")

    while True:
        choice = input("Введите номер файла: ").strip()
        if not choice.isdigit():
            print("Ошибка: введите число.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(files):
            return files[idx - 1]
        print(f"Ошибка: введите число от 1 до {len(files)}.")


def main():
    script_dir = Path(__file__).resolve().parent

    files = find_files(script_dir)
    target = choose_file(files)

    print(f"Открываю: {target}")
    lst_trace = []
    first_line_sql = False
    timestamp, db, process_id, thread_number, attachment, user, process_name, transaction, event, time_execute, sql_text = (
        'Время', 'База данных', 'Идентификатор процесса', 'Номер в рамках потока', 'Attachment',
        'Пользователь', 'Имя процесса', 'Транзакция', 'Событие', 'Время выполнения в мс',
        'SQL')

    with open(target, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            match_timestamp = re.match(
                r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{4})\s\((?P<process_id>[\w:]+)#?(?P<thread_number>\d+)?\)\s(?P<event>[ \w]+)',
                line)
            if match_timestamp:
                lst_trace.append(
                    [timestamp, db, process_id, thread_number, attachment, user, process_name, transaction,
                     event, time_execute, sql_text.strip()])
                timestamp, process_id, thread_number, event, db, attachment, user, process_name, transaction, sql_text, time_execute = ('',) * 11
                timestamp = match_timestamp.group("timestamp")
                process_id = match_timestamp.group("process_id")
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
            match_proc = re.search(r'^\s*(?P<process_name>[-_a-zA-Zа-яА-Я\d\s\[\]/\\().:,\'"]+):[-]?\d+$', line)
            if match_proc:
                process_name = match_proc.group('process_name')
                continue
            match_transaction = re.search(r'\(TRA_(?P<transaction>\d+),[\s\w|]+\)$', line)
            if match_transaction:
                transaction = match_transaction.group('transaction')
                continue
            if event == 'EXECUTE_PROCEDURE_FINISH':  # если событие процедуры, то ищем строку процедуры
                match_sql = re.search(r'(?P<sql_text>Procedure [_a-zA-Z0-9]+):', line)
                if match_sql:
                    sql_text = match_sql.group('sql_text')
            match_sql = re.search(r'[-]{79}',
                                  line)  # SQL текст заключен между символами ---- и ^^^^. Определяем конец и начало SQL
            match_end_sql = re.search(r'[\^]{79}', line)
            if match_end_sql:
                first_line_sql = False
                continue
            match_end_sql = re.search(r'\d+ records fetched without sorting', line)
            if match_end_sql:
                first_line_sql = False
                continue
            if first_line_sql:
                sql_text += ' ' + line.strip()
                continue
            if match_sql:
                first_line_sql = True
                sql_text = ''
                match_sql = None
                continue
            match_execute = re.search(r'\s*(?P<time_execute>\d+)\sms[\s,]', line)
            if match_execute:
                time_execute = match_execute.group('time_execute')

    # Пишем последнюю запись после цикла
    lst_trace.append(
        [timestamp, db, process_id, thread_number, attachment, user, process_name, transaction,
         event, time_execute, sql_text.strip()])

    target_out = f'{target}' + f'_{datetime.now():%Y-%m-%d_%H-%M-%S}.csv'
    print(f'Запись в файл: {target_out}')
    with open(f'{target_out}', 'w', newline='', encoding='cp1251', errors="replace") as out_file:
        writer = csv.writer(out_file, quotechar='"', delimiter=';')
        for line in lst_trace:
            writer.writerow(line)
    print(f'Файл записан: {target_out}')


if __name__ == "__main__":
    main()
