-- Tabla: Pacientes
CREATE TABLE Pacientes (
    id_paciente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(10),
    telefono VARCHAR(15),
    direccion TEXT,
    email VARCHAR(100),
    seguro_medico VARCHAR(100)
);

-- Tabla: Centros_Salud
CREATE TABLE Centros_Salud (
    id_centro SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    zona VARCHAR(50),
    telefono VARCHAR(15),
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6)
);

-- Tabla: Especialidades
CREATE TABLE Especialidades (
    id_especialidad SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla: Medicos
CREATE TABLE Medicos (
    id_medico SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    numero_colegiatura VARCHAR(50) NOT NULL,
    id_especialidad INT REFERENCES Especialidades(id_especialidad),
    id_centro INT REFERENCES Centros_Salud(id_centro)
);

-- Tabla: Horarios
CREATE TABLE Horarios (
    id_horario SERIAL PRIMARY KEY,
    id_medico INT REFERENCES Medicos(id_medico),
    dia_semana VARCHAR(15) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

-- Tabla: Citas
CREATE TABLE Citas (
    id_cita SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES Pacientes(id_paciente),
    id_medico INT REFERENCES Medicos(id_medico),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(50),
    motivo TEXT
);

-- Tabla: Usuarios
CREATE TABLE Usuarios (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol VARCHAR(50) NOT NULL
);