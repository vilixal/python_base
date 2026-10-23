#!/usr/bin/env python3
"""
Считает количество строк в файле, содержащих заданный шаблон.

Использование:
    python count_lines.py input.log
    python count_lines.py input.log "свой шаблон"
"""

import sys
from pathlib import Path

# Шаблон по умолчанию
DEFAULT_PATTERN = ",INFO,MvvAnswerBuilder,No customer data"


def count_lines(input_path: Path, pattern: str) -> int:
    count = 0
    with input_path.open("r", encoding="utf-8", errors="replace") as fin:
        for line in fin:
            if pattern in line:
                count += 1
    return count


def main() -> int:
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print(f"Использование: {sys.argv[0]} <input.log> [шаблон]")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.is_file():
        print(f"Ошибка: файл '{input_path}' не найден.")
        return 2

    input_path2 = Path(sys.argv[2])
    input_path3 = Path(sys.argv[3])

    pattern = sys.argv[4] if len(sys.argv) == 3 else DEFAULT_PATTERN
    count = count_lines(input_path, pattern)
    count2 = count_lines(input_path2, pattern)
    count3 = count_lines(input_path3, pattern)

    print(f"Шаблон:  {pattern}")
    print(f"Найдено: {count+count2+count3}")
    return 0


if __name__ == "__main__":
    sys.exit(main())