-- Crear tabla administradores
CREATE TABLE administradores (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    nombre TEXT NOT NULL,
    cedula TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla profesores
CREATE TABLE profesores (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    nombre TEXT NOT NULL,
    cedula TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    aprobado BOOLEAN DEFAULT FALSE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla estudiantes
CREATE TABLE estudiantes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    nombre TEXT NOT NULL,
    cedula TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    aprobado BOOLEAN DEFAULT FALSE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear indices para mejorar rendimiento en busquedas por cedula
CREATE INDEX idx_administradores_cedula ON administradores(cedula);
CREATE INDEX idx_profesores_cedula ON profesores(cedula);
CREATE INDEX idx_estudiantes_cedula ON estudiantes(cedula);

-- Eliminar administradores anteriores si existen
DELETE FROM administradores WHERE cedula = '123456789';
DELETE FROM administradores WHERE nombre = 'igual';
DELETE FROM administradores WHERE nombre LIKE '%igual%';

-- Agregar columna aprobado a tablas existentes si no existe
ALTER TABLE profesores ADD COLUMN IF NOT EXISTS aprobado BOOLEAN DEFAULT FALSE;
ALTER TABLE estudiantes ADD COLUMN IF NOT EXISTS aprobado BOOLEAN DEFAULT FALSE;

-- Insertar administrador por defecto
INSERT INTO administradores (nombre, cedula, email, password) VALUES
('Administrador Principal', '123456789', 'admin@icfespro.com', 'administrador123123456789'); -- password: administrador123123456789 (plain text)
