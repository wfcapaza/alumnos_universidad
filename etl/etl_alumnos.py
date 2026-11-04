import csv
import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
from calculos import (calcular_estado_academico, calcular_condicion_beca)

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "data"
    / "alumnos_universidad_sucio_v2.csv"
)

load_dotenv(BASE_DIR / ".env")

class ETLAlumnos:

    def __init__(self):

        self.registros_extraidos = []
        self.registros_transformados = []
        self.ids_vistos = set()
        self.descartados = {
            "duplicados": 0,
            "vacios": 0,
            "semestre_invalido": 0,
            "promedio_invalido": 0,
            "creditos_invalidos": 0
        }

    def extraer(self):

        print("\n===== EXTRACT =====")

        try:

            with open(
                CSV_PATH,
                mode="r",
                encoding="utf-8-sig",
                newline=""
            ) as archivo:

                lector = csv.DictReader(archivo)
                self.registros_extraidos = list(lector)

                print(f"Registros extraídos: {len(self.registros_extraidos)}")

        except FileNotFoundError:

            print(f"ERROR: No se encontró el archivo: {CSV_PATH}")
            raise

        except Exception as error:

            print(f"ERROR al leer el CSV: {error}")
            raise

    def limpiar_texto(self, valor):

        texto = valor.strip()
        texto = " ".join(texto.split())
        return texto.title()

    def transformar(self):

        print("\n===== TRANSFORM =====")
        self.registros_transformados = []

        for fila in self.registros_extraidos:
            # 1. Limpiar ID
            id_alumno = (fila["id_alumno"].strip().upper())

            # 2. Detectar duplicados
            if id_alumno in self.ids_vistos:

                self.descartados["duplicados"] += 1
                continue

            self.ids_vistos.add(id_alumno)

            # 3. Obtener campos como texto
            nombre = fila["nombre_completo"].strip()
            facultad = fila["facultad"].strip()
            carrera = fila["carrera"].strip()
            semestre_texto = fila["semestre"].strip()
            promedio_texto = fila["promedio_ponderado"].strip()
            creditos_texto = fila["creditos_matriculados"].strip()

            # 4. Validar campos vacíos
            if (id_alumno == "" 
                or nombre == ""
                or facultad == ""
                or carrera == ""
                or semestre_texto == ""
                or promedio_texto == ""
                or creditos_texto == ""
            ):
                
                self.descartados["vacios"] += 1
                continue

            # 5. Convertir semestre
            try:
                semestre = int(semestre_texto)

            except ValueError:
                self.descartados["semestre_invalido"] += 1
                continue

            # 6. Validar semestre 1 - 10
            if semestre < 1 or semestre > 10:

                self.descartados["semestre_invalido"] += 1
                continue

            # 7. Convertir promedio
            try:
                promedio = float(promedio_texto)

            except ValueError:
                self.descartados["promedio_invalido"] += 1
                continue

            # 8. Validar promedio 0 - 20
            if promedio < 0 or promedio > 20:

                self.descartados["promedio_invalido"] += 1
                continue

            # 9. Convertir créditos
            try:
                creditos = int(creditos_texto)

            except ValueError:
                self.descartados["creditos_invalidos"] += 1
                continue


            if creditos < 0:
                self.descartados["creditos_invalidos"] += 1
                continue

            # 10. Normalizar textos
            nombre = self.limpiar_texto(nombre)
            facultad = self.limpiar_texto(facultad)
            carrera = self.limpiar_texto(carrera)

            # 11. Campos calculados
            estado_academico = (calcular_estado_academico(promedio))
            condicion_beca = (calcular_condicion_beca(promedio, creditos))

            # 12. Crear registro final
            registro = (
                id_alumno,
                nombre,
                facultad,
                carrera,
                semestre,
                round(promedio, 2),
                creditos,
                estado_academico,
                condicion_beca
            )

            self.registros_transformados.append(registro)


        print(f"Registros válidos: {len(self.registros_transformados)}")
        print(f"Duplicados descartados: {self.descartados['duplicados']}")
        print(f"Registros con vacíos: {self.descartados['vacios']}")
        print(f"Semestres inválidos: {self.descartados['semestre_invalido']}")
        print(f"Promedios inválidos: {self.descartados['promedio_invalido']}")
        print(f"Créditos inválidos: {self.descartados['creditos_invalidos']}")

    def conectar(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def cargar(self):
        print("\n===== LOAD =====")
        conexion = None
        cursor = None

        try:
            conexion = self.conectar()
            cursor = conexion.cursor()

            sql = """
                INSERT INTO alumnos (
                    id_alumno,
                    nombre_completo,
                    facultad,
                    carrera,
                    semestre,
                    promedio_ponderado,
                    creditos_matriculados,
                    estado_academico,
                    condicion_beca
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            cursor.executemany(sql, self.registros_transformados)
            conexion.commit()

            print(f"Registros insertados en MySQL: {cursor.rowcount}")

        except mysql.connector.Error as error:
            if conexion is not None:
                conexion.rollback()

            print(f"ERROR al cargar en MySQL: {error}")
            print("Se ejecutó rollback().")
            raise

        finally:
            if cursor is not None:
                cursor.close()

            if (conexion is not None and conexion.is_connected()):
                conexion.close()

            print("Conexión MySQL cerrada.")

    def ejecutar(self):

        print("======================================")
        print("ETL ALUMNOS UNIVERSIDAD")
        print("======================================")

        self.extraer()
        self.transformar()
        self.cargar()

        print("\n======================================")
        print("ETL FINALIZADO")
        print("======================================")

        print(f"Procesados: {len(self.registros_extraidos)}")
        print(f"Cargados: {len(self.registros_transformados)}")
        print(f"Descartados: {len(self.registros_extraidos) - len(self.registros_transformados)}")

if __name__ == "__main__":
    etl = ETLAlumnos()
    etl.ejecutar()