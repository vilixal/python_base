#!/usr/bin/env python3
"""
Фильтрует строки в лог-файле по заданной подстроке.

Использование:
    python filter_log.py input.log
    python filter_log.py input.log output.log
"""

import sys
from pathlib import Path

# Подстрока, которую ищем в строках
NEEDLE = ",DefaultQuartzScheduler_Worker-9,"
# '''
# NEEDLES = (
# ",multi-11000000059-pool-5-thread-123,",
# ",multi-11000000059-pool-5-thread-124,",
# )
# ...
# if any(n in line for n in NEEDLES):
# '''


def filter_log(input_path: Path, output_path: Path, needle: str = NEEDLE) -> int:
    """
    Читает input_path, записывает в output_path только те строки,
    которые содержат needle. Возвращает количество найденных строк.
    """
    count = 0
    # newline="" сохраняет оригинальные переводы строк (\n и \r\n) без изменений
    with input_path.open("r", encoding="utf-8", errors="replace", newline="") as fin, \
         output_path.open("w", encoding="utf-8", newline="") as fout:
        for line in fin:
            if needle in line:
                fout.write(line)
                count += 1
    return count


def main() -> int:
    # if len(sys.argv) < 2 or len(sys.argv) > 3:
    #     print(f"Использование: {sys.argv[0]} <input.log> [output.log]")
    #     return 1

    input_path = Path(sys.argv[1])
    if not input_path.is_file():
        print(f"Ошибка: файл '{input_path}' не найден.")
        return 2

    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_name(input_path.stem + "_filtered.log")

    found = filter_log(input_path, output_path)

    print(f"Входной файл:  {input_path}")
    print(f"Выходной файл: {output_path}")
    print(f"Найдено строк: {found}")
    return 0


if __name__ == "__main__":
    sys.exit(main())