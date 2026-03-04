from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class Especialidad(BaseModel):
    id_especialidad: int
    nombre: str

# Modelo para CREAR (sin id, la BD lo genera)
class EspecialidadCrear(BaseModel):
    nombre: str

# RUTAS
@router.get("/")
async def listar_especialidades(conn = Depends(get_conexion)):
    consulta = "SELECT id_especialidad, nombre FROM Especialidades"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar especialidades")

@router.post("/")
async def insertar_especialidad(especialidad: EspecialidadCrear, conn = Depends(get_conexion)):
    consulta = "INSERT INTO Especialidades (nombre) VALUES (%s)"
    parametros = (especialidad.nombre,)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Especialidad registrada correctamente"}
    except Exception as e:
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar la especialidad")

@router.put("/{id_especialidad}")
async def actualizar_especialidad(id_especialidad: int, especialidad: Especialidad, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Especialidades
    SET nombre=%s
    WHERE id_especialidad=%s
    """
    parametros = (especialidad.nombre, id_especialidad)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Especialidad no encontrada")
            await conn.commit()
            return {"mensaje": "Especialidad actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_especialidad}")
async def eliminar_especialidad(id_especialidad: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Especialidades WHERE id_especialidad=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_especialidad,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Especialidad no encontrada")
            await conn.commit()
            return {"mensaje": "Especialidad eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")