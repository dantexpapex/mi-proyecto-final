from fastapi import APIRouter, Depends, HTTPException
from config.conexionbd import get_conexion

router = APIRouter()

# 1️⃣ REPORTE GENERAL DE ESPECIALIDADES
@router.get("/especialidades")
async def reporte_especialidades(conn = Depends(get_conexion)):

    consulta = """
    SELECT 
        e.id_especialidad,
        e.nombre AS especialidad,
        COUNT(c.id_cita) AS total_citas
    FROM especialidades e
    LEFT JOIN medicos m 
        ON e.id_especialidad = m.id_especialidad
    LEFT JOIN citas c 
        ON m.id_medico = c.id_medico
    GROUP BY e.id_especialidad, e.nombre
    ORDER BY e.id_especialidad;
    """

    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            datos = await cursor.fetchall()
            return {"Reporte General de Especialidades": datos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2️⃣ REPORTE INDIVIDUAL DE ESPECIALIDAD
@router.get("/especialidades/{id_especialidad}")
async def reporte_especialidad(id_especialidad: int, conn = Depends(get_conexion)):

    consulta = """
    SELECT 
        m.id_medico,
        m.nombre,
        m.apellido,
        COUNT(c.id_cita) AS total_citas
    FROM medicos m
    LEFT JOIN citas c 
        ON m.id_medico = c.id_medico
    WHERE m.id_especialidad = %s
    GROUP BY m.id_medico, m.nombre, m.apellido
    ORDER BY total_citas DESC;
    """

    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_especialidad,))
            datos = await cursor.fetchall()
            return {"Reporte Individual de Especialidad": datos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 3️⃣ RANKING DE MEDICOS
@router.get("/medicos")
async def ranking_medicos(conn = Depends(get_conexion)):

    consulta = """
    SELECT 
        m.id_medico,
        m.nombre,
        m.apellido,
        COUNT(c.id_cita) AS total_citas
    FROM medicos m
    LEFT JOIN citas c 
        ON m.id_medico = c.id_medico
    GROUP BY m.id_medico, m.nombre, m.apellido
    ORDER BY total_citas DESC;
    """

    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            datos = await cursor.fetchall()
            return {"ranking_medicos": datos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))