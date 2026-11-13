import pprint
from pprint import pp

import firebird.driver as fdb  # Для Firebird 3+. Для старых версий: import fdb

# --- Параметры подключения ---
DB_DSN = 'localhost:ncore-bank'
DB_USER = 'SYSDBA'
DB_PASS = 'masterkey'
LIST_LINK=['UNIFO_PAYMENT']


def get_all_relations():
    # Подключение (пример для firebird-driver)
    con = fdb.connect(database=DB_DSN, user=DB_USER, password=DB_PASS)
    cur = con.cursor()

    # ------------------------------------------------------------------
    # 1. Поиск ВСЕХ ПРЕДКОВ (движение вверх по sys_objects)
    # ------------------------------------------------------------------
    sql_parent = """
        SELECT sobj_name, sobj_kind, sobj_name_parent
        FROM sys_objects
        WHERE sobj_kind = 'TBL' and sobj_name = ?
    """
    sql_links = """        
            SELECT sobj_name, soln_type, sobj_name_dest
            FROM sys_objlink
            WHERE (soln_type = 'CHD' or soln_type = 'DET' or soln_type = 'OWN') and soln_subsystem='BANK_CLIENT' and sobj_name = ?
            union all
            SELECT sobj_name, soln_type, sobj_name_dest
            FROM sys_objlink
            WHERE (soln_type = 'CHD' or soln_type = 'DET' or soln_type = 'OWN') and soln_subsystem='BANK_CLIENT' and SOBJ_NAME_DEST = ?
        """
    # OWN (от главного объекта к подчиненному) OWN – сноска
    # DET (от подчиненного к главному) DET-Детейл
    # CHD (от подчиненного к главному) CHD-Потомок
    for obj in LIST_LINK:
        print(f'=== Проверяем {obj} ===')
        cur.execute(sql_parent, (obj,))
        ancestors = cur.fetchall()
        for row in ancestors:
            print(f"{row[0]} -> родитель '{row[1]}': {row[2]}")
            if row[2] not in LIST_LINK and row[2]:
                LIST_LINK.append(row[2])

        cur.execute(sql_links, (obj,obj))
        links = cur.fetchall()
        for row in links:
            print(f"{row[0]} -> {row[1]} {row[2]}")
            if row[2] not in LIST_LINK and row[2]:
                LIST_LINK.append(row[2])
            if row[0] not in LIST_LINK and row[0]:
                LIST_LINK.append(row[0])

    pp(LIST_LINK)
    con.close()


if __name__ == "__main__":
    get_all_relations()