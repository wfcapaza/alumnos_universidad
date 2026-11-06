import { AfterViewInit, Component, ElementRef, OnDestroy, ViewChild } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import Chart from 'chart.js/auto';
import { AlumnoService } from '../../services/alumno.service';

@Component({
  selector: 'app-dashboard',
  imports: [MatCardModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements AfterViewInit, OnDestroy {
  @ViewChild('graficoFacultades')
  graficoFacultadesRef!: ElementRef<HTMLCanvasElement>;

  @ViewChild('graficoEstado')
  graficoEstadoRef!: ElementRef<HTMLCanvasElement>;

  private graficoFacultades?: Chart;
  private graficoEstado?: Chart;

  constructor(private alumnoService: AlumnoService) {}

  ngAfterViewInit(): void {
    this.cargarGraficoFacultades();
    this.cargarGraficoEstado();
  }

  cargarGraficoFacultades(): void {
    this.alumnoService.obtenerAlumnosPorFacultad().subscribe({
      next: (datos) => {
        const facultades = datos.map((item) => item.facultad);
        const cantidades = datos.map((item) => item.cantidad);

        this.graficoFacultades = new Chart(this.graficoFacultadesRef.nativeElement, {
          type: 'bar',
          data: {
            labels: facultades,
            datasets: [
              {
                label: 'Cantidad de alumnos',
                data: cantidades,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      },

      error: (error) => {
        console.error('Error al cargar gráfico de facultades', error);
      },
    });
  }

  cargarGraficoEstado(): void {
    this.alumnoService.obtenerEstadoAcademico().subscribe({
      next: (datos) => {
        const estados = datos.map((item) => item.estado_academico);
        const cantidades = datos.map((item) => item.cantidad);

        this.graficoEstado = new Chart(this.graficoEstadoRef.nativeElement, {
          type: 'doughnut',
          data: {
            labels: estados,
            datasets: [
              {
                label: 'Alumnos',
                data: cantidades,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      },

      error: (error) => {
        console.error('Error al cargar gráfico de estado académico', error);
      },
    });
  }

  ngOnDestroy(): void {
    this.graficoFacultades?.destroy();
    this.graficoEstado?.destroy();
  }
}
