from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class CentroSalud(BaseModel):
    id_centro: int
    nombre: str
    direccion: str
    zona: str
    telefono: str
    latitud: float
    longitud: float

# Modelo para CREAR (sin id, la BD lo genera)
class CentroSaludCrear(BaseModel):
    nombre: str
    direccion: str
    zona: str
    telefono: str
    latitud: float
    longitud: float

# RUTAS
@router.get("/")
async def listar_centros_salud(conn = Depends(get_conexion)):
    consulta = "SELECT id_centro, nombre, direccion, zona, telefono, latitud, longitud FROM Centros_Salud"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar centros de salud")

@router.post("/")
async def insertar_centro_salud(centro: CentroSaludCrear, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Centros_Salud (
        nombre, direccion, zona, telefono, latitud, longitud
    ) VALUES (%s, %s, %s, %s, %s, %s)
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
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el centro de salud")

@router.put("/{id_centro}")
async def actualizar_centro_salud(id_centro: int, centro: CentroSalud, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Centros_Salud
    SET nombre=%s,
        direccion=%s,
        zona=%s,
        telefono=%s,
        latitud=%s,
        longitud=%s
    WHERE id_centro=%s
    """
    parametros = (
        centro.nombre,
        centro.direccion,
        centro.zona,
        centro.telefono,
        centro.latitud,
        centro.longitud,
        id_centro
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Centro de salud no encontrado")
            await conn.commit()
            return {"mensaje": "Centro de salud actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_centro}")
async def eliminar_centro_salud(id_centro: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Centros_Salud WHERE id_centro=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_centro,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Centro de salud no encontrado")
            await conn.commit()
            return {"mensaje": "Centro de salud eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")