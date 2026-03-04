from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class Medico(BaseModel):
    id_medico: int
    nombre: str
    apellido: str
    numero_colegiatura: str
    id_especialidad: int
    id_centro: int

# Modelo para CREAR (sin id, la BD lo genera)
class MedicoCrear(BaseModel):
    nombre: str
    apellido: str
    numero_colegiatura: str
    id_especialidad: int
    id_centro: int

# RUTAS
@router.get("/")
async def listar_medicos(conn = Depends(get_conexion)):
    consulta = "SELECT id_medico, nombre, apellido, numero_colegiatura, id_especialidad, id_centro FROM Medicos"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar médicos")

@router.post("/")
async def insertar_medico(medico: MedicoCrear, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Medicos (
        nombre, apellido, numero_colegiatura, id_especialidad, id_centro
    ) VALUES (%s, %s, %s, %s, %s)
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
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el médico")

@router.put("/{id_medico}")
async def actualizar_medico(id_medico: int, medico: Medico, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Medicos
    SET nombre=%s,
        apellido=%s,
        numero_colegiatura=%s,
        id_especialidad=%s,
        id_centro=%s
    WHERE id_medico=%s
    """
    parametros = (
        medico.nombre,
        medico.apellido,
        medico.numero_colegiatura,
        medico.id_especialidad,
        medico.id_centro,
        id_medico
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Médico no encontrado")
            await conn.commit()
            return {"mensaje": "Médico actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_medico}")
async def eliminar_medico(id_medico: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Medicos WHERE id_medico=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_medico,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Médico no encontrado")
            await conn.commit()
            return {"mensaje": "Médico eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")