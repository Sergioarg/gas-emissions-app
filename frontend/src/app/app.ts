import { Component, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { EmissionApi } from './data/emission.api';
import { Emission } from './core/models/emissions';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('emissions-frontend');

  constructor(private emissionApi: EmissionApi) {}

  ngOnInit(): void {
    console.log('🚀 Iniciando llamada al servicio de emisiones...');

    this.emissionApi.getEmissions().subscribe({
      next: (emissions: Emission[]) => {
        console.log('✅ Datos recibidos correctamente del backend:', emissions);
        console.log('📊 Total de emisiones:', emissions.length);
      },
      error: (error) => {
        console.error('❌ Error al obtener emisiones:', error);
      }
    });
  }
}
