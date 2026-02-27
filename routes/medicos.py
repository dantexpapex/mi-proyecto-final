from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO
class Medico(BaseModel):
    id_medico: int
    nombre: str
    apellido: str
    numero_colegiatura: str
    id_especialidad: int
    id_centro: int

# RUTAS
@router.get("/")
async def listar_medicos(conn = Depends(get_conexion)):
    consulta = "SELECT * FROM Medicos"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar")

@router.post("/")
async def insertar_medico(medico: Medico, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Medicos (
        nombre, apellido, numero_colegiatura, id_especialidad, id_centro
    ) VALUES (%s, %s, %s, %s, %s)
    RETURNING *
    """
    parametros = (
        medico.nombre,
        medico.apellido,
        medico.numero_colegiatura,
        medico.id_especialidad,
        medico.id_centro
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Médico registrado correctamente"}
    except Exception as e:
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar")