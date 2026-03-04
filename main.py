from fastapi import FastAPI
from config.conexionbd import app
from routes import centros_salud, citas, especialidades, horarios, medicos,usuarios, pacientes
from fastapi.middleware.cors import CORSMiddleware  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)
app.include_router(centros_salud.router, prefix="/centros_salud")
app.include_router(citas.router, prefix="/citas")
app.include_router(especialidades.router, prefix="/especialidades")
app.include_router(horarios.router, prefix="/horarios")
app.include_router(medicos.router, prefix="/medicos")
app.include_router(usuarios.router, prefix="/usuarios")
app.include_router(pacientes.router, prefix="/pacientes")





