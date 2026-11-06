import { Component, OnInit } from '@angular/core';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Alumno } from '../../models/alumno';
import { AlumnoService } from '../../services/alumno.service';

@Component({
  selector: 'app-alumnos',
  imports: [MatTableModule, MatFormFieldModule, MatInputModule],
  templateUrl: './alumnos.html',
  styleUrl: './alumnos.css',
})
export class Alumnos implements OnInit {
  columnas: string[] = [
    'id_alumno',
    'nombre_completo',
    'facultad',
    'carrera',
    'semestre',
    'promedio_ponderado',
    'creditos_matriculados',
    'estado_academico',
    'condicion_beca',
  ];

  dataSource = new MatTableDataSource<Alumno>([]);

  constructor(private alumnoService: AlumnoService) {}

  ngOnInit(): void {
    this.cargarAlumnos();
  }

  cargarAlumnos(): void {
    this.alumnoService.obtenerAlumnos().subscribe({
      next: (alumnos) => {
        this.dataSource.data = alumnos;
        console.log('Alumnos recibidos:', alumnos.length);
      },

      error: (error) => {
        console.error('Error al obtener alumnos', error);
      },
    });
  }

  aplicarFiltro(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;

    this.dataSource.filter = valor.trim().toLowerCase();
  }
}
