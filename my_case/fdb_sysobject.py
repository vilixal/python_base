import pprint
from pprint import pp
from collections import defaultdict
import firebird.driver as fdb  # Для Firebird 3+. Для старых версий: import fdb


# --- Параметры подключения ---
DB_DSN = 'localhost:ncore-bank'
DB_USER = 'SYSDBA'
DB_PASS = 'masterkey'
LIST_TABLE=['UNIFO_PAYMENT']
LIST_LINK=[]


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

def get_all_relations():
    # Подключение (пример для firebird-driver)
    con = fdb.connect(database=DB_DSN, user=DB_USER, password=DB_PASS)
    cur = con.cursor()

    # ------------------------------------------------------------------
    # 1. Поиск ВСЕХ ПРЕДКОВ (движение вверх по sys_objects)
    # ------------------------------------------------------------------
    sql_parent = """
        SELECT sobj_name, 'Предок',sobj_kind, sobj_name_parent, 'ID'
        FROM sys_objects
        WHERE sobj_kind = 'TBL' and sobj_name = ?
    """
    sql_links = """        
            SELECT sln.sobj_name,sln.soln_caption,sln.soln_type,sln.sobj_name_dest,sos.sfld_name
            FROM sys_objlink sln
            join sys_objects so on so.sobj_name=sln.SOBJ_NAME_DEST
            join SYS_OBJLINK_SEGMENT sos on sos.sobj_name=sln.sobj_name and sos.soln_name=sln.soln_name
            WHERE (sln.soln_type = 'CHD' or sln.soln_type = 'OWN') and so.sobj_subsystem <> 'NCORE' and sln.sobj_name = ? and (so.sobj_is_system <> 1 or so.sobj_is_system is null) and so.sobj_kind='TBL' 
            union all
            SELECT sln.sobj_name,sln.soln_caption,sln.soln_type,sln.sobj_name_dest,sos.sfld_name
            FROM sys_objlink sln
            join sys_objects so on so.sobj_name=sln.sobj_name
            join SYS_OBJLINK_SEGMENT sos on sos.sobj_name=sln.sobj_name and sos.soln_name=sln.soln_name
            WHERE (sln.soln_type = 'CHD' or sln.soln_type = 'DET') and so.sobj_subsystem<>'NCORE' and sln.SOBJ_NAME_DEST = ? and (so.sobj_is_system <> 1 or so.sobj_is_system is null) and so.sobj_kind='TBL' 
        """
    # OWN (от главного объекта к подчиненному) OWN – сноска (в главном объекте есть ИД, ссылающийся на другой подчиненный объект (вроде как 1 к 1))
    # DET (от подчиненного к главному) DET-Детейл (то есть ИД в подчиненном ссылается на гланвый (много к 1)
    # CHD (от подчиненного к главному) CHD-Потомок (так же ИД в подчиненном, но объекты могут быть из другой области, поэтому нужно еще анализировать подход для отдельных случаев)
    for obj in LIST_TABLE:
        print(f'=== Проверяем {obj} ===')
        cur.execute(sql_parent, (obj,))
        ancestors = cur.fetchall()
        for row in ancestors:
            print(f"{row[0]} -> родитель '{row[2]}': {row[3]}")
            if row[3] not in LIST_TABLE and row[3]:
                LIST_TABLE.append(row[3])
            if [row[0],row[1],row[2],row[3],row[4]] not in LIST_LINK and row[3]:
                LIST_LINK.append([row[0], row[1], row[2], row[3], row[4]])
        cur.execute(sql_links, (obj,obj))
        links = cur.fetchall()
        for row in links:
            print(f"{row[0]} -> {row[2]} {row[3]}")
            if row[3] not in LIST_TABLE and row[3]:
                LIST_TABLE.append(row[3])
            if row[0] not in LIST_TABLE and row[0]:
                LIST_TABLE.append(row[0])
            if [row[0],row[1],row[2],row[3],row[4]] not in LIST_LINK:
                LIST_LINK.append([row[0], row[1], row[2], row[3], row[4]])

    # pp(LIST_TABLE)
    # for i in LIST_LINK:
    #     print(i)
    print_matrix(LIST_LINK)
    print_tree(LIST_LINK, 'UNIFO_PAYMENT')
    con.close()


if __name__ == "__main__":
    get_all_relations()