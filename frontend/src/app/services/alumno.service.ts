import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Alumno, AlumnosPorFacultad, EstadoAcademicoResumen } from '../models/alumno';

@Injectable({
  providedIn: 'root',
})
export class AlumnoService {
  private readonly apiUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  obtenerAlumnos(): Observable<Alumno[]> {
    return this.http.get<Alumno[]>(`${this.apiUrl}/alumnos`);
  }

  obtenerAlumnosPorFacultad(): Observable<AlumnosPorFacultad[]> {
    return this.http.get<AlumnosPorFacultad[]>(`${this.apiUrl}/dashboard/facultades`);
  }

  obtenerEstadoAcademico(): Observable<EstadoAcademicoResumen[]> {
    return this.http.get<EstadoAcademicoResumen[]>(`${this.apiUrl}/dashboard/estado-academico`);
  }
}
