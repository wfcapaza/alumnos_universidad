
from repositorio import AlumnoRepositorio

class AlumnoServicio:

    def __init__(self):
        self.repositorio = AlumnoRepositorio()

    def listar_alumnos(self):
        return self.repositorio.listar_alumnos()

    def obtener_alumnos_por_facultad(self):
        return self.repositorio.obtener_alumnos_por_facultad()

    def obtener_estado_academico(self):
        return self.repositorio.obtener_estado_academico()
