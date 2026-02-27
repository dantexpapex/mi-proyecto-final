from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO
class CentroSalud(BaseModel):
    id_centro: int
    nombre: str
    direccion: str
    zona: str
    telefono: str
    latitud: float
    longitud: float

# RUTAS
@router.get("/")
async def listar_centros_salud(conn = Depends(get_conexion)):
    consulta = "SELECT * FROM Centros_Salud"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar")

@router.post("/")
async def insertar_centro_salud(centro: CentroSalud, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Centros_Salud (
        nombre, direccion, zona, telefono, latitud, longitud
    ) VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING *
    """
    parametros = (
        centro.nombre,
        centro.direccion,
        centro.zona,
        centro.telefono,
        centro.latitud,
        centro.longitud
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Centro de salud registrado correctamente"}
    except Exception as e:
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar")