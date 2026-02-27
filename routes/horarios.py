from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO
class Horario(BaseModel):
    id_horario: int
    id_medico: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str

# RUTAS
@router.get("/")
async def listar_horarios(conn = Depends(get_conexion)):
    consulta = "SELECT * FROM Horarios"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar")

@router.post("/")
async def insertar_horario(horario: Horario, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Horarios (
        id_medico, dia_semana, hora_inicio, hora_fin
    ) VALUES (%s, %s, %s, %s)
    RETURNING *
    """
    parametros = (
        horario.id_medico,
        horario.dia_semana,
        horario.hora_inicio,
        horario.hora_fin
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Horario registrado correctamente"}
    except Exception as e:
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar")