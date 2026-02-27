
# Ejemplo de procesos asincronicos
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from contextlib import asynccontextmanager
# prodPSYN3Pool
# DB_URL = "postgresql://usuario:password@host:puerto/nameBD"
DB_URL = "postgresql://postgres:dantex@localhost:5432/bd_entrenamiento?options=-csearch_path%3Dpublic" 
# 1. Gestionamos el ciclo de vida del Pool
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se crea el pool al iniciar la app
    app.async_pool = AsyncConnectionPool(conninfo=DB_URL, open=False)
    try:
        await app.async_pool.open()
        print("✅ Pool de conexiones abierto exitosamente")
        yield
    finally:
        # Esto asegura que se cierre el pool al apagar la app, incluso  si la app falla al arrancar
        await app.async_pool.close() 
        print("🛑 Pool de conexiones cerrado")

app = FastAPI(lifespan=lifespan)

# 2. Dependencia para inyectar la conexión en las rutas
async def get_conexion():
    async with app.async_pool.connection() as conn:
        # Configuramos dict_row para recibir diccionarios en lugar de tuplas
        conn.row_factory = dict_row
        yield conn

# BaseModel clase fundamental para definir modelos
class Producto(BaseModel):
    id_producto:int
    id_tipo:int
    descripcion:str
    precio_compra:float
    precio_venta:float
    cantidad:int
    activo:bool

@app.get("/producto/")
async def listar(conn = Depends(get_conexion)):
    consulta = "Select id_producto,id_tipo,descripcion,precio_compra,precio_venta,cantidad,activo from tproducto"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado gral de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error, consulte con su Administrador")

@app.post("/producto/")
async def insert_producto(producto: Producto,conn = Depends(get_conexion)):
    consulta = "insert into tproducto(id_producto,id_tipo,descripcion,precio_compra,precio_venta,cantidad) values(%s,%s,%s,%s,%s,%s)"
    parametros = (producto.id_producto,producto.id_tipo,producto.descripcion,producto.precio_compra,producto.precio_venta,producto.cantidad)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Producto registrado exitosamente"}
    except Exception as e:
        print(f"Error imprevisto de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="La operacion de insercion no se efectuo, consulte con su Administrador")
