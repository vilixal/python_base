from nicegui import app
import asyncpg

DB_POOL: asyncpg.Pool = None


#@app.on_startup #на старт приложения
async def init_pool():
    global DB_POOL
    try:
        if DB_POOL is None:

            DB_POOL = await asyncpg.create_pool(
                user='postgres',
                password='masterkey',
                database='isup',
                host='localhost',
                timeout=10
            )
            print(f"Подключение к PostgreSQL установлено: {DB_POOL._connect_kwargs}")
        else:
            print("Подключение уже существует")
    except Exception as e:
        ui.label(f'Ошибка: {e}')
        ui.label('Проверьте подключение к базе данных')


async def get_columns(table_name):
    if DB_POOL is None:
        await init_pool()
    async with DB_POOL.acquire() as conn:
        list_columns = await conn.fetch(f'''SELECT column_name -- имя поля
                                       FROM information_schema.columns
                                       WHERE table_name = $1 -- Укажите имя вашей таблицы
                                         AND table_schema = 'public' -- Обычно 'public', если не используете другие схемы
                                       ORDER BY ordinal_position;''',table_name)
        columns = []
        for row in list_columns:
            columns.append(row[0])
        print(f'Получили список полей для таблицы {table_name}: {columns}')
        return columns


async def get_data(table_name: str, where_dict: dict = None,order: dict = None):
    if DB_POOL is None:
        await init_pool()
    where = None
    if where_dict:
        for key, value in where_dict.items():
            where=f'where {key} = {value}'
    async with DB_POOL.acquire() as conn:
        rows = await conn.fetch(f'SELECT * FROM {table_name} {where} ORDER BY id')
        print(f'Получили данные таблицы {table_name}: {rows}')
        return [dict(row) for row in rows]


async def add_data(table_name: str, data: dict, where: dict = None):
    if DB_POOL is None:
        await init_pool()
    columns,values = '',''
    for key, value in data.items():
        if key != 'id':
            columns=','.join(key)
            values=','.join(value)
    async with DB_POOL.acquire() as conn:
        rows=await conn.fetchrow(f'INSERT INTO {table_name} ({columns}) VALUES ($1) RETURNING id',values)
        print(f'Вставили в таблицу{table_name} значения {data} под ID = {rows}')
        return dict(rows)


@app.on_shutdown
async def close_db_pool():
    # Закрываем пул при остановке приложения
    if DB_POOL:
        await DB_POOL.close()
        print("Соединение с БД закрыто")
    else:
        print("Соединение с БД не может быть закрыто, так как не существует")


