export interface Alumno {
    id_alumno: string;
    nombre_completo: string;
    facultad: string;
    carrera: string;
    semestre: number;
    promedio_ponderado: number;
    creditos_matriculados: number;
    estado_academico: string;
    condicion_beca: string;
}

export interface AlumnosPorFacultad {
    facultad: string;
    cantidad: number;
}

export interface EstadoAcademicoResumen {
    estado_academico: string;
    cantidad: number;
}
