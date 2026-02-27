from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO
class Especialidad(BaseModel):
    id_especialidad: int
    nombre: str

# RUTAS
@router.get("/")
async def listar_especialidades(conn = Depends(get_conexion)):
    consulta = "SELECT * FROM Especialidades"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar")

@router.post("/")
async def insertar_especialidad(especialidad: Especialidad, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Especialidades (
        nombre
    ) VALUES (%s)
    RETURNING *
    """
    parametros = (
        especialidad.nombre,
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Especialidad registrada correctamente"}
    except Exception as e:
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar")