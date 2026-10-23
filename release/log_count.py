#!/usr/bin/env python3
"""
Ищет в текстовом логе строки с "ExternalDbAnswerBuilder,DEBTOR_NAME->",
извлекает ФИО (всё до символа ';') и выводит те ФИО, которые
встречаются в файле больше одного раза, с указанием количества.

Использование:
    python count_fio.py input.log
"""

import re
import sys
from collections import Counter
from pathlib import Path

# Якорь, после которого начинается ФИО
ANCHOR = "ExternalDbAnswerBuilder,DEBTOR_NAME->"

# Компилируем один раз — быстрее на больших логах.
# Захватываем всё до первой ';' (не жадный .*?)
PATTERN = re.compile(re.escape(ANCHOR) + r"(.*?);")


def extract_fio(line: str) -> str | None:
    """Возвращает ФИО из строки или None, если якорь/ФИО не найдены."""
    m = PATTERN.search(line)
    if not m:
        return None
    fio = m.group(1).strip()
    return fio or None


def main() -> int:
    # if len(sys.argv) != 2:
    #     print(f"Использование: {sys.argv[0]} <input.log>")
    #     return 1

    input_path = Path(sys.argv[1])
    if not input_path.is_file():
        print(f"Ошибка: файл '{input_path}' не найден.")
        return 2

    input_path2 = Path(sys.argv[2])
    input_path3 = Path(sys.argv[3])

    counter: Counter[str] = Counter()
    total_lines = 0
    matched_lines = 0

    with input_path.open("r", encoding="utf-8", errors="replace") as fin:
        for line in fin:
            total_lines += 1
            if ANCHOR not in line:
                continue
            fio = extract_fio(line)
            if fio:
                counter[fio] += 1
                matched_lines += 1

    with input_path2.open("r", encoding="utf-8", errors="replace") as fin:
        for line in fin:
            total_lines += 1
            if ANCHOR not in line:
                continue
            fio = extract_fio(line)
            if fio:
                counter[fio] += 1
                matched_lines += 1

    with input_path3.open("r", encoding="utf-8", errors="replace") as fin:
        for line in fin:
            total_lines += 1
            if ANCHOR not in line:
                continue
            fio = extract_fio(line)
            if fio:
                counter[fio] += 1
                matched_lines += 1

    # Оставляем только те, что встречаются чаще одного раза
    duplicates = {fio: n for fio, n in counter.items() if n > 1}

    print(f"Всего строк в файле:        {total_lines}")
    print(f"Строк с DEBTOR_NAME->:      {matched_lines}")
    print(f"Уникальных ФИО:             {len(counter)}")
    print(f"ФИО, встречающихся > 1 раза: {len(duplicates)}")
    print("-" * 60)

    if not duplicates:
        print("Дубликатов не найдено.")
        return 0

    # Сортировка по убыванию частоты, затем по алфавиту
    for fio, n in sorted(duplicates.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n:>6}  {fio}")

    return 0


if __name__ == "__main__":
    sys.exit(main())