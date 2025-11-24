import { Component, signal } from '@angular/core';
import { EmissionsChartComponent } from './presentation/emissions-chart/emissions-chart.component';

@Component({
  selector: 'app-root',
  imports: [EmissionsChartComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('Gas Emissions Dashboard - Technical Test');
}
