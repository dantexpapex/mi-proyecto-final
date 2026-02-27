from fastapi import FastAPI
from config.conexionbd import app
from routes import producto, persona, servicios
from fastapi.middleware.cors import CORSMiddleware  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)
app.include_router(producto.router, prefix="/producto")
app.include_router(persona.router, prefix="/persona")
app.include_router(servicios.router, prefix="/servicios")





