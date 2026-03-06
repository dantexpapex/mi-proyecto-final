from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from config.configuracion import config

DB_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?options=-csearch_path%3Dpublic"

pool = AsyncConnectionPool(conninfo=DB_URL, open=False)

async def get_conexion():
    async with pool.connection() as conn:
        conn.row_factory = dict_row
        yield conn