from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import centros_salud, citas, especialidades, horarios, medicos, usuarios, pacientes, reportes
from config.conexionbd import pool

app = FastAPI()

@app.on_event("startup")
async def startup():
    await pool.open()
    print("✅ Pool de conexiones abierto")

@app.on_event("shutdown")
async def shutdown():
    await pool.close()
    print("🛑 Pool cerrado")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(centros_salud.router, prefix="/centros_salud")
app.include_router(citas.router, prefix="/citas")
app.include_router(especialidades.router, prefix="/especialidades")
app.include_router(horarios.router, prefix="/horarios")
app.include_router(medicos.router, prefix="/medicos")
app.include_router(usuarios.router, prefix="/usuarios")
app.include_router(pacientes.router, prefix="/pacientes")
app.include_router(reportes.router, prefix="/reportes")