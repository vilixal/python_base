from collections import defaultdict

# LIST_LINK: [source, caption, type, dest, field]
# type: 'TBL'(предок) | 'DET'(детейл) | 'OWN'(сноска) | 'CHD'(потомок)

TYPE_STYLE = {
    'TBL': ('↑', 'Предок  (1:1, PK)'),
    'OWN': ('→', 'Сноска  (1:1, FK в source)'),
    'DET': ('←', 'Детейл  (N:1, FK в dest)'),
    'CHD': ('⇢', 'Потомок (N:1, межобластная)'),
}
TYPE_ORDER = ['TBL', 'OWN', 'CHD', 'DET']  # порядок отображения


def print_matrix(links):
    """Матрица: строки — объекты-источники, колонки — типы связей."""
    by_src = defaultdict(lambda: defaultdict(list))
    for src, caption, typ, dst, fld in links:
        by_src[src][typ].append((dst, fld, caption))

    print("\n=== МАТРИЦА СВЯЗЕЙ ===\n")
    header = f"{'ОБЪЕКТ':<38} | " + " | ".join(f"{TYPE_STYLE[t][0]} {t:<3}" for t in TYPE_ORDER)
    print(header)
    print("-" * len(header))
    for src in sorted(by_src):
        cells = []
        for t in TYPE_ORDER:
            items = by_src[src].get(t, [])
            cells.append(", ".join(d for d, _, _ in items) if items else "·")
        print(f"{src:<38} | " + " | ".join(f"{c:<6}" if c == "·" else c for c in cells))


def print_tree(links, root, max_depth=10):
    """Дерево обхода от корня (без повторов)."""
    # индекс: source -> [(type, dest, field, caption)]
    fwd = defaultdict(list)
    for src, caption, typ, dst, fld in links:
        fwd[src].append((typ, dst, fld, caption))

    seen = set()

    def walk(node, depth, prefix, marker=''):
        if depth > max_depth:
            return
        children = [c for c in fwd.get(node, []) if c[1] not in seen]
        # сортируем: сначала TBL, потом OWN, CHD, DET
        children.sort(key=lambda c: TYPE_ORDER.index(c[0]))
        for i, (typ, dst, fld, cap) in enumerate(children):
            last = (i == len(children) - 1)
            branch = '└── ' if last else '├── '
            arrow, _ = TYPE_STYLE[typ]
            seen.add(dst)
            print(f"{prefix}{marker}{branch}[{typ}] {dst}  ({fld})  «{cap}»")
            walk(dst, depth + 1, prefix + ('    ' if last else '│   '))

    print(f"\n=== ДЕРЕВО ОТ {root} ===\n")
    print(f"{root}")
    seen.add(root)
    walk(root, 0, "")


# --- Использование ---
# (вставьте сюда ваш LIST_LINK после обхода, либо соберите его в get_all_relations)
print_matrix(LIST_LINK)
print_tree(LIST_LINK, 'UNIFO_PAYMENT')