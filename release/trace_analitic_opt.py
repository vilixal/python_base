import csv
import re
import sys
from datetime import datetime
from pathlib import Path

# ---- Скомпилированные регулярки ----
RE_TS = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{4})\s'
    r'\((?P<process_id>[\w:]+)#?(?P<thread_number>\d+)?\)\s'
    r'(?P<event>[ \w]+)'
)
RE_ATT = re.compile(
    r'(?P<db>[-a-zA-Z0-9_/\.]+)\s\(ATT_(?P<attachment>\d+),\s'
    r'(?P<user>[-a-zA-Z0-9_]+):\w+,\s\w+,\s'
)
RE_PROC = re.compile(r'^\s*(?P<process_name>[-_a-zA-Zа-яА-Я\d\s\[\]/\\().:,\'"]+):[-]?\d+$')
RE_TRA = re.compile(r'\(TRA_(?P<transaction>\d+),[\s\w|]+\)$')
RE_PROC_SQL = re.compile(r'(?P<sql_text>Procedure [_a-zA-Z0-9]+):')
RE_SQL_START = re.compile(r'[-]{79}')
RE_SQL_END = re.compile(r'[\^]{79}')
RE_RECORDS = re.compile(r'\d+ records fetched without sorting')
RE_EXEC = re.compile(r'\s*(?P<time_execute>\d+)\sms[\s,]')


def find_files(directory: Path):
    files = list(directory.glob("*.txt")) + list(directory.glob("*.fbtrace_text"))
    return sorted(files)


def choose_file(files):
    if not files:
        print("В каталоге нет файлов .txt или .fbtrace_text")
        sys.exit(1)
    if len(files) == 1:
        print(f"Найден один файл: {files[0].name}")
        return files[0]
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


def _progress(total_bytes, done_bytes, start_time):
    """Печатает строку прогресса в одну строку."""
    if total_bytes <= 0:
        return
    # защита от случая, когда винда возвращает в done_bytes 2^64 значение
    if done_bytes>total_bytes:
        done_bytes = total_bytes
    pct = min(100.0, done_bytes * 100.0 / total_bytes)
    elapsed = max(0.01, datetime.now().timestamp() - start_time)
    speed = done_bytes / elapsed / 1024 / 1024  # MB/s
    bar_len = 30
    filled = int(bar_len * pct / 100)
    bar = '#' * filled + '-' * (bar_len - filled)
    sys.stdout.write(
        f"\r[{bar}] {pct:5.1f}%  {done_bytes/1024/1024:8.1f} / "
        f"{total_bytes/1024/1024:.1f} MB  {speed:5.1f} MB/s"
    )
    sys.stdout.flush()


def parse_trace(target: Path):
    """Парсит трейс, возвращает список записей."""
    lst_trace = []
    first_line_sql = False
    sql_parts = []
    total_bytes = target.stat().st_size
    start_ts = datetime.now().timestamp()
    last_update = 0.0

    # Поля первой записи
    timestamp, db, process_id, thread_number, attachment, user, process_name, transaction, event, time_execute, sql_text = (
        'Время', 'База данных', 'Идентификатор процесса', 'Номер в рамках потока', 'Attachment',
        'Пользователь', 'Имя процесса', 'Транзакция', 'Событие', 'Время выполнения в мс',
        'SQL')

    def flush_record():
        lst_trace.append([
            timestamp, db, process_id, thread_number, attachment, user,
            process_name, transaction, event, time_execute,
            ' '.join(sql_parts).strip() if sql_parts else sql_text.strip(),
        ])

    #пишем первую строку и зануляем timestamp
    flush_record()
    timestamp = db = process_id = thread_number = attachment = user = ''
    process_name = transaction = event = time_execute = ''
    sql_text = ''

    with open(target, "r", encoding="utf-8", errors="replace") as file:
        while True:
            line = file.readline()
            if not line:
                break

            # ---- прогресс не чаще 10 раз в секунду ----
            now = datetime.now().timestamp()
            if now - last_update > 0.1:
                _progress(total_bytes, file.tell(), start_ts)
                last_update = now

            # ---- быстрые проверки перед регулярками ----
            if line[:4].isdigit() and len(line) > 11 and line[10] == 'T':
                m = RE_TS.match(line)
                if m:
                    if timestamp:  # завершаем предыдущую запись
                        flush_record()
                    # сброс полей
                    timestamp = m.group("timestamp")
                    process_id = m.group("process_id")
                    thread_number = m.group("thread_number") or ''
                    event = m.group("event")
                    db = attachment = user = process_name = ''
                    transaction = time_execute = sql_text = ''
                    sql_parts = []
                    first_line_sql = False
                    continue

            if first_line_sql:
                if line.startswith('^' * 79) or 'records fetched without sorting' in line:
                    first_line_sql = False
                    continue
                sql_parts.append(line.strip())
                # конец SQL-блока
                continue

            if 'ATT_' in line:
                m = RE_ATT.search(line)
                if m:
                    db = m.group('db')
                    attachment = m.group('attachment')
                    user = m.group('user')
                    continue

            if 'TRA_' in line:
                m = RE_TRA.search(line)
                if m:
                    transaction = m.group('transaction')
                    continue

            if line and line[0].isspace() and line.rstrip().endswith(tuple('0123456789')):
                # потенциально имя процесса (заканчивается на :число)
                m = RE_PROC.match(line)
                if m:
                    process_name = m.group('process_name')
                    continue

            if event == 'EXECUTE_PROCEDURE_FINISH':
                m = RE_PROC_SQL.search(line)
                if m:
                    sql_text = m.group('sql_text')
                    continue

            if '----' in line:
                m = RE_SQL_START.search(line)
                if m:
                    first_line_sql = True
                    sql_parts = []
                    continue

            if 'ms' in line:
                m = RE_EXEC.search(line)
                if m:
                    time_execute = m.group('time_execute')

    # прогресс 100%
    _progress(total_bytes, total_bytes, start_ts)
    sys.stdout.write('\n')

    if timestamp:
        flush_record()
    return lst_trace


def main():
    script_dir = Path(__file__).resolve().parent
    files = find_files(script_dir)
    target = choose_file(files)

    print(f"Открываю: {target}")
    lst_trace = parse_trace(target)

    target_out = f'{target}_{datetime.now():%Y-%m-%d_%H-%M-%S}.csv'
    print(f'Запись в файл: {target_out}')
    with open(target_out, 'w', newline='', encoding='cp1251', errors="replace") as out_file:
        writer = csv.writer(out_file, quotechar='"', delimiter=';')
        writer.writerows(lst_trace)
    print(f'Файл записан: {target_out}')


if __name__ == "__main__":
    main()