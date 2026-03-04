from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class Paciente(BaseModel):
    id_paciente: int
    nombre: str
    apellido: str
    fecha_nacimiento: str
    genero: str
    telefono: str
    direccion: str
    email: str
    seguro_medico: str

# Modelo para CREAR (sin id, la BD lo genera)
class PacienteCrear(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: str
    genero: str
    telefono: str
    direccion: str
    email: str
    seguro_medico: str

# RUTAS
@router.get("/")
async def listar_pacientes(conn = Depends(get_conexion)):
    consulta = "SELECT id_paciente, nombre, apellido, fecha_nacimiento, genero, telefono, direccion, email, seguro_medico FROM Pacientes"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar pacientes")

@router.post("/")
async def insertar_paciente(paciente: PacienteCrear, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Pacientes (
        nombre, apellido, fecha_nacimiento, genero, telefono, direccion, email, seguro_medico
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    parametros = (
        paciente.nombre,
        paciente.apellido,
        paciente.fecha_nacimiento,
        paciente.genero,
        paciente.telefono,
        paciente.direccion,
        paciente.email,
        paciente.seguro_medico
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Paciente registrado correctamente"}
    except Exception as e:
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el paciente")

@router.put("/{id_paciente}")
async def actualizar_paciente(id_paciente: int, paciente: Paciente, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Pacientes
    SET nombre=%s,
        apellido=%s,
        fecha_nacimiento=%s,
        genero=%s,
        telefono=%s,
        direccion=%s,
        email=%s,
        seguro_medico=%s
    WHERE id_paciente=%s
    """
    parametros = (
        paciente.nombre,
        paciente.apellido,
        paciente.fecha_nacimiento,
        paciente.genero,
        paciente.telefono,
        paciente.direccion,
        paciente.email,
        paciente.seguro_medico,
        id_paciente
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Paciente no encontrado")
            await conn.commit()
            return {"mensaje": "Paciente actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_paciente}")
async def eliminar_paciente(id_paciente: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Pacientes WHERE id_paciente=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_paciente,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Paciente no encontrado")
            await conn.commit()
            return {"mensaje": "Paciente eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")