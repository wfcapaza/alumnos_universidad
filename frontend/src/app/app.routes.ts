import { Routes } from '@angular/router';
import { Alumnos } from './pages/alumnos/alumnos';
import { Dashboard } from './pages/dashboard/dashboard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'alumnos',
    pathMatch: 'full',
  },

  {
    path: 'alumnos',
    component: Alumnos,
  },

  {
    path: 'dashboard',
    component: Dashboard,
  },

  {
    path: '**',
    redirectTo: 'alumnos',
  },
];
