from nicegui import app
import asyncpg

DB_POOL: asyncpg.Pool = None


@app.on_startup
async def init_pool():
    global DB_POOL
    DB_POOL = await asyncpg.create_pool(
        user='postgres',
        password='masterkey',
        database='isup',
        host='localhost'
    )
    print("Подключение к PostgreSQL установлено")


async def get_banks():
    async with DB_POOL.acquire() as conn:
        return await conn.fetch("SELECT * FROM banklist ORDER BY bank_name")


# async def add_bank(name: str, status: str = 'active'):
#     async with DB_POOL.acquire() as conn:
#         return await conn.fetchrow(
#             "INSERT INTO banklist (bank_name, status) VALUES ($1, $2) RETURNING id",
#             name, status
#         )


async def get_servers_for_bank(bank_id: int):
    async with DB_POOL.acquire() as conn:
        return await conn.fetch(
            "SELECT * FROM server WHERE banklist_id = $1",
            bank_id
        )

@app.on_shutdown
async def close_db_pool():
    # Закрываем пул при остановке приложения
    await DB_POOL.close()
    print("Соединение с БД закрыто")