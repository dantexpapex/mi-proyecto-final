from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO
class Cita(BaseModel):
    id_cita: int
    id_paciente: int
    id_medico: int
    fecha: str
    hora: str
    estado: str
    motivo: str

# RUTAS
@router.get("/")
async def listar_citas(conn = Depends(get_conexion)):
    consulta = "SELECT * FROM Citas"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar")

@router.post("/")
async def insertar_cita(cita: Cita, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Citas (
        id_paciente, id_medico, fecha, hora, estado, motivo
    ) VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING *
    """
    parametros = (
        cita.id_paciente,
        cita.id_medico,
        cita.fecha,
        cita.hora,
        cita.estado,
        cita.motivo
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Cita registrada correctamente"}
    except Exception as e:
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar")