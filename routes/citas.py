from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class Cita(BaseModel):
    id_cita: int
    id_paciente: int
    id_medico: int
    fecha: str
    hora: str
    estado: str
    motivo: str

# Modelo para CREAR (sin id, la BD lo genera)
class CitaCrear(BaseModel):
    id_paciente: int
    id_medico: int
    fecha: str
    hora: str
    estado: str
    motivo: str

# RUTAS
@router.get("/")
async def listar_citas(conn = Depends(get_conexion)):
    consulta = "SELECT id_cita, id_paciente, id_medico, fecha, hora, estado, motivo FROM Citas"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar citas")

@router.post("/")
async def insertar_cita(cita: CitaCrear, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Citas (
        id_paciente, id_medico, fecha, hora, estado, motivo
    ) VALUES (%s, %s, %s, %s, %s, %s)
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
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar la cita")

@router.put("/{id_cita}")
async def actualizar_cita(id_cita: int, cita: Cita, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Citas
    SET id_paciente=%s,
        id_medico=%s,
        fecha=%s,
        hora=%s,
        estado=%s,
        motivo=%s
    WHERE id_cita=%s
    """
    parametros = (
        cita.id_paciente,
        cita.id_medico,
        cita.fecha,
        cita.hora,
        cita.estado,
        cita.motivo,
        id_cita
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Cita no encontrada")
            await conn.commit()
            return {"mensaje": "Cita actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_cita}")
async def eliminar_cita(id_cita: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Citas WHERE id_cita=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_cita,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Cita no encontrada")
            await conn.commit()
            return {"mensaje": "Cita eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")