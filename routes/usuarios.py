from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from config.conexionbd import get_conexion

router = APIRouter()

# MODELO completo (incluye id para PUT)
class Usuario(BaseModel):
    id_usuario: int
    username: str
    password_hash: str
    rol: str

# Modelo para CREAR (sin id, la BD lo genera)
class UsuarioCrear(BaseModel):
    username: str
    password_hash: str
    rol: str

# RUTAS
@router.get("/")
async def listar_usuarios(conn = Depends(get_conexion)):
    consulta = "SELECT id_usuario, username, password_hash, rol FROM Usuarios"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al listar usuarios")

@router.post("/")
async def insertar_usuario(usuario: UsuarioCrear, conn = Depends(get_conexion)):
    consulta = """
    INSERT INTO Usuarios (
        username, password_hash, rol
    ) VALUES (%s, %s, %s)
    """
    parametros = (
        usuario.username,
        usuario.password_hash,
        usuario.rol
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Usuario registrado correctamente"}
    except Exception as e:
        await conn.rollback()
        print(f"Error insertar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo insertar el usuario")

@router.put("/{id_usuario}")
async def actualizar_usuario(id_usuario: int, usuario: Usuario, conn = Depends(get_conexion)):
    consulta = """
    UPDATE Usuarios
    SET username=%s,
        password_hash=%s,
        rol=%s
    WHERE id_usuario=%s
    """
    parametros = (
        usuario.username,
        usuario.password_hash,
        usuario.rol,
        id_usuario
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            await conn.commit()
            return {"mensaje": "Usuario actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error actualizar: {e}")
        raise HTTPException(status_code=400, detail="La actualización no se efectuó")

@router.delete("/{id_usuario}")
async def eliminar_usuario(id_usuario: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM Usuarios WHERE id_usuario=%s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_usuario,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            await conn.commit()
            return {"mensaje": "Usuario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error eliminar: {e}")
        raise HTTPException(status_code=400, detail="La eliminación no se efectuó")