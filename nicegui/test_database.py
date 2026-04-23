import asyncio
import asyncpg
import datetime

async def main():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect('postgresql://postgres@localhost/isup?password=masterkey')

    # Insert a record into the created table.
    # await conn.execute('''
    #     INSERT INTO users(name, dob) VALUES($1, $2)
    # ''', 'Bob', datetime.date(1984, 3, 1))
    # await conn.execute("""
    #                        INSERT INTO banklist (bank_name, status, app_version,db_version)
    #                        VALUES ($1, $2, $3,$4)
    #                        """, 'Совкомбанк', 'Disable', '1.9.33.0','5.0.3')
    # Select a row from the table.
    table_name = 'banklist'
    list_column = await conn.fetch('''
    SELECT 
    column_name        -- имя поля
    FROM 
    information_schema.columns
    WHERE 
    table_name = $1        -- Укажите имя вашей таблицы
    AND table_schema = 'public' -- Обычно 'public', если не используете другие схемы
    ORDER BY 
    ordinal_position;
    ''',table_name)
    column=''
    for row in list_column:
        if column=='':
            column=row[0]
        else:
            column=column+','+row[0]
    print(column)
    rows = await conn.fetch(
        f'SELECT {column} FROM banklist')# WHERE id = $1', 1)

    # *row* now contains
    print(list_column)
    print([dict(row) for row in rows])
    # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))

    # Close the connection.
    await conn.close()

asyncio.run(main())
