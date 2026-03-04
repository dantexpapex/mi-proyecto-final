from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class Horario(BaseModel):
    id_horario: int
    id_medico: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str

# Modelo para CREAR (sin id, la BD lo genera)
class HorarioCrear(BaseModel):
    id_medico: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str

# RUTAS
@router.get("/")
async def listar_horarios(conn = Depends(get_conexion)):
    consulta = "SELECT id_horario, id_medico, dia_semana, hora_inicio, hora_fin FROM Horarios"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar horarios")

@router.post("/")
async def insertar_horario(horario: HorarioCrear, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Horarios (
        id_medico, dia_semana, hora_inicio, hora_fin
    ) VALUES (%s, %s, %s, %s)
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
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el horario")

@router.put("/{id_horario}")
async def actualizar_horario(id_horario: int, horario: Horario, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Horarios
    SET id_medico=%s,
        dia_semana=%s,
        hora_inicio=%s,
        hora_fin=%s
    WHERE id_horario=%s
    """
    parametros = (
        horario.id_medico,
        horario.dia_semana,
        horario.hora_inicio,
        horario.hora_fin,
        id_horario
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Horario no encontrado")
            await conn.commit()
            return {"mensaje": "Horario actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_horario}")
async def eliminar_horario(id_horario: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Horarios WHERE id_horario=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_horario,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Horario no encontrado")
            await conn.commit()
            return {"mensaje": "Horario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")