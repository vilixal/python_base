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
            SELECT sln.sobj_name, sln.soln_type, sln.sobj_name_dest
            FROM sys_objlink sln
            join sys_objects so on sln.SOBJ_NAME_DEST=so.sobj_name
            WHERE (sln.soln_type = 'CHD' or sln.soln_type = 'OWN') and so.sobj_subsystem <> 'NCORE' and sln.sobj_name = ? and (so.sobj_is_system <> 1 or so.sobj_is_system is null) and so.sobj_kind='TBL' --or sln.soln_type = 'DET'-дает верхние объекты (из запроса в пакет)
            union all
            SELECT sln.sobj_name, sln.soln_type, sln.sobj_name_dest
            FROM sys_objlink sln
            join sys_objects so on sln.sobj_name=so.sobj_name
            WHERE (sln.soln_type = 'CHD' or sln.soln_type = 'DET') and so.sobj_subsystem<>'NCORE' and sln.SOBJ_NAME_DEST = ? and (so.sobj_is_system <> 1 or so.sobj_is_system is null) and so.sobj_kind='TBL' --or sln.soln_type = 'OWN' тоже
        """
    # OWN (от главного объекта к подчиненному) OWN – сноска (в главном объекте есть ИД, ссылающийся на другой подчиненный объект (вроде как 1 к 1))
    # DET (от подчиненного к главному) DET-Детейл (то есть ИД в подчиненном ссылается на гланвый (много к 1)
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