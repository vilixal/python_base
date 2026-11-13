import firebird.driver as fdb  # Для Firebird 3+. Для старых версий: import fdb

# --- Параметры подключения ---
DB_DSN = 'localhost:ncore-bank'
DB_USER = 'SYSDBA'
DB_PASS = 'masterkey'
TARGET_OBJECT = 'UNIFO_PAYMENT'


def get_all_relations(target_name):
    # Подключение (пример для firebird-driver)
    con = fdb.connect(database=DB_DSN, user=DB_USER, password=DB_PASS)
    cur = con.cursor()

    # ------------------------------------------------------------------
    # 1. Поиск ВСЕХ ПРЕДКОВ (движение вверх по sys_objects)
    # ------------------------------------------------------------------
    sql_ancestors = """
    WITH RECURSIVE ancestors (sobj_name, sobj_name_parent, lvl) AS (
        -- Якорь: прямой предок целевого объекта
        SELECT sobj_name, sobj_name_parent, 1
        FROM sys_objects
        WHERE sobj_kind = 'TBL' and sobj_name = ?

        UNION ALL

        -- Рекурсия: ищем предка для найденного предка
        SELECT o.sobj_name, o.sobj_name_parent, a.lvl + 1
        FROM sys_objects o
        JOIN ancestors a ON o.sobj_name = a.sobj_name_parent
        WHERE a.sobj_name_parent IS NOT NULL
    )
    SELECT sobj_name, sobj_name_parent, lvl FROM ancestors
    """

    print(f"--- Предки (Ancestors) для {target_name} ---")
    cur.execute(sql_ancestors, (target_name,))
    ancestors = cur.fetchall()
    for row in ancestors:
        print(f"Уровень {row[2]}: {row[0]} -> родитель: {row[1]}")

    # ------------------------------------------------------------------
    # 2. Поиск ВСЕХ ВЛОЖЕННЫХ СВЯЗЕЙ (sys_objlink)
    # ------------------------------------------------------------------
    # Примечание: здесь строим цепочку "объект -> dest -> dest2 ..."
    sql_links = """
    WITH RECURSIVE obj_links (source, dest, lvl) AS (
        -- Якорь: прямые связи из sys_objlink для целевого объекта
        SELECT sobj_name, sobj_name_dest, 1
        FROM sys_objlink
        WHERE (soln_type = 'CHD' or soln_type = 'DET' or soln_type = 'OWN') and sobj_name = ?

        UNION ALL

        -- Рекурсия: связи для найденных dest-объектов
        SELECT l.sobj_name, l.sobj_name_dest, ol.lvl + 1
        FROM sys_objlink l
        JOIN obj_links ol ON l.sobj_name = ol.dest
        where (soln_type = 'CHD' or soln_type = 'DET' or soln_type = 'OWN')
    )
    SELECT source, dest, lvl FROM obj_links
    """

    print(f"\n--- Вложенные связи (ObjLinks) для {target_name} ---")
    cur.execute(sql_links, (target_name,))
    links = cur.fetchall()
    for row in links:
        print(f"Уровень {row[2]}: {row[0]} -> {row[1]}")

    # ------------------------------------------------------------------
    # 3. (Опционально) Вложенные связи ПРЕДКОВ
    # ------------------------------------------------------------------
    # Можно объединить логику, но часто проще сделать отдельный запрос,
    # передав список найденных предков. Если предков немного, можно
    # выполнить запрос для каждого или использовать IN.
    if ancestors:
        # Собираем уникальные имена предков (включая исходный объект, если нужно)
        ancestor_names = list({row[0] for row in ancestors})
        # Добавляем целевой объект для полноты
        ancestor_names.append(target_name)

        # Формируем плейсхолдеры для IN (?)
        placeholders = ','.join(['?'] * len(ancestor_names))

        sql_ancestor_links = f"""
        WITH RECURSIVE anc_links (source, dest, lvl) AS (
            SELECT sobj_name, sobj_name_dest, 1
            FROM sys_objlink
            WHERE (soln_type = 'CHD' or soln_type = 'DET' or soln_type = 'OWN') and sobj_name IN ({placeholders})

            UNION ALL

            SELECT l.sobj_name, l.sobj_name_dest, al.lvl + 1
            FROM sys_objlink l
            JOIN anc_links al ON l.sobj_name = al.dest
            where (soln_type = 'CHD' or soln_type = 'DET' or soln_type = 'OWN') 
        )
        SELECT source, dest, lvl FROM anc_links
        """

        print(f"\n--- Связи предков (Links of Ancestors) ---")
        with con.cursor() as cur_anc:
            cur_anc.execute(sql_ancestor_links, ancestor_names)
            for row in cur_anc.fetchall():
                print(f"Уровень {row[2]}: {row[0]} -> {row[1]}")

    con.close()


if __name__ == "__main__":
    get_all_relations(TARGET_OBJECT)