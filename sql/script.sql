CREATE DATABASE IF NOT EXISTS universidad_db;

USE universidad_db;


CREATE TABLE IF NOT EXISTS alumnos (
    id_alumno VARCHAR(15) PRIMARY KEY,
    nombre_completo VARCHAR(120) NOT NULL,
    facultad VARCHAR(100) NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INT NOT NULL,
    promedio_ponderado DECIMAL(4,2) NOT NULL,
    creditos_matriculados INT NOT NULL,
    estado_academico VARCHAR(30) NOT NULL,
    condicion_beca VARCHAR(30) NOT NULL
);

SELECT * FROM alumnos