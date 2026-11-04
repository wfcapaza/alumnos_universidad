import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

load_dotenv(BASE_DIR / ".env")

class AlumnoRepositorio:

    def conectar(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def listar_alumnos(self):
        conexion = self.conectar()
        cursor = conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    id_alumno,
                    nombre_completo,
                    facultad,
                    carrera,
                    semestre,
                    promedio_ponderado,
                    creditos_matriculados,
                    estado_academico,
                    condicion_beca
                FROM alumnos
                ORDER BY id_alumno
            """

            cursor.execute(sql)
            alumnos = cursor.fetchall()

            for alumno in alumnos:
                alumno["promedio_ponderado"] = float(alumno["promedio_ponderado"])

            return alumnos

        finally:
            cursor.close()
            conexion.close()

    def obtener_alumnos_por_facultad(self):
        conexion = self.conectar()
        cursor = conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    facultad,
                    COUNT(*) AS cantidad
                FROM alumnos
                GROUP BY facultad
                ORDER BY cantidad DESC
            """

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()

    def obtener_estado_academico(self):
        conexion = self.conectar()
        cursor = conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    estado_academico,
                    COUNT(*) AS cantidad
                FROM alumnos
                GROUP BY estado_academico
                ORDER BY cantidad DESC
            """

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            cursor.close()
            conexion.close()