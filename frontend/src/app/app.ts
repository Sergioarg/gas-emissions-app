import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { EmissionsChartComponent } from './presentation/emissions-chart/emissions-chart.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, EmissionsChartComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('Gas Emissions Dashboard - Technical Test');
}
