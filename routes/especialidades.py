from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion
import traceback

router = APIRouter()

# --- MODELOS ---

# Modelo completo (para respuestas y PUT)
class Especialidad(BaseModel):
    id_especialidad: int
    nombre: str

# Modelo para creación (POST)
class EspecialidadCrear(BaseModel):
    nombre: str

# --- RUTAS CRUD ---

# 1. OBTENER TODAS LAS ESPECIALIDADES
@router.get("/")
async def obtener_especialidades(conn = Depends(get_conexion)):
    consulta = "SELECT id_especialidad, nombre FROM Especialidades"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            datos = await cursor.fetchall()
            return datos
    except Exception as e:
        print(f"Error al obtener: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la lista de especialidades")

# 2. OBTENER UNA ESPECIALIDAD POR ID
@router.get("/{id_especialidad}")
async def obtener_especialidad_por_id(id_especialidad: int, conn = Depends(get_conexion)):
    consulta = "SELECT id_especialidad, nombre FROM Especialidades WHERE id_especialidad = %s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_especialidad,))
            resultado = await cursor.fetchone()
            if not resultado:
                raise HTTPException(status_code=404, detail="Especialidad no encontrada")
            return resultado
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al buscar: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# 3. CREAR UNA NUEVA ESPECIALIDAD
@router.post("/")
async def crear_especialidad(especialidad: EspecialidadCrear, conn = Depends(get_conexion)):
    consulta = "INSERT INTO Especialidades (nombre) VALUES (%s)"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (especialidad.nombre,))
            await conn.commit()
            return {"mensaje": "Especialidad creada correctamente", "id": cursor.lastrowid}
    except Exception as e:
        print(f"Error al crear: {e}")
        raise HTTPException(status_code=400, detail="No se pudo crear la especialidad")

# 4. ACTUALIZAR ESPECIALIDAD
@router.put("/{id_especialidad}")
async def actualizar_especialidad(id_especialidad: int, especialidad: EspecialidadCrear, conn = Depends(get_conexion)):
    consulta = "UPDATE Especialidades SET nombre=%s WHERE id_especialidad=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (especialidad.nombre, id_especialidad))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Especialidad no encontrada")
            await conn.commit()
            return {"mensaje": "Especialidad actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

# 5. ELIMINAR ESPECIALIDAD
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
        print(f"Error al eliminar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo eliminar (es posible que esté siendo usada por un médico)")