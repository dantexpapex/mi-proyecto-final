from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO
class Usuario(BaseModel):
    id_usuario: int
    username: str
    password_hash: str
    rol: str

# RUTAS
@router.get("/")
async def listar_usuarios(conn = Depends(get_conexion)):
    consulta = "SELECT * FROM Usuarios"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar")

@router.post("/")
async def insertar_usuario(usuario: Usuario, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Usuarios (
        username, password_hash, rol
    ) VALUES (%s, %s, %s)
    RETURNING *
    """
    parametros = (
        usuario.username,
        usuario.password_hash,
        usuario.rol
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Usuario registrado correctamente"}
    except Exception as e:
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar")