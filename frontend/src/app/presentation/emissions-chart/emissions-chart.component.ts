import { Component, OnInit, OnDestroy, ElementRef, ViewChild, AfterViewInit, ChangeDetectorRef, PLATFORM_ID, Inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import * as d3 from 'd3';
import { EmissionApi } from '../../data/emission.api';
import { Emission } from '../../core/models/emissions';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-emissions-chart',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatChipsModule,
    MatCardModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './emissions-chart.component.html',
  styleUrl: './emissions-chart.component.css'
})
export class EmissionsChartComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('chartContainer', { static: false }) chartContainer!: ElementRef;

  private destroy$ = new Subject<void>();
  public loading = true;
  public error: string | null = null;
  private svg: any;
  private margin = { top: 20, right: 80, bottom: 60, left: 80 };
  private width = 800;
  private height = 400;
  private emissionsData: Emission[] | null = null;

  public selectedCountry: string | null = null;
  public selectedActivity: string | null = null;
  public selectedEmissionType: string | null = null;
  public availableCountries: string[] = [];
  public availableActivities: string[] = [];
  public availableEmissionTypes: string[] = [];

  constructor(
    private emissionApi: EmissionApi,
    private cdr: ChangeDetectorRef,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit(): void {
    this.loadEmissions();
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      if (this.chartContainer?.nativeElement && !this.loading) {
        this.initChart();
        if (this.emissionsData) {
          this.processData(this.emissionsData);
        }
      }
    }, 100);
  }

  ngOnDestroy(): void {
    d3.select('.emissions-tooltip').remove();
    this.destroy$.next();
    this.destroy$.complete();
  }

  private initChart(): void {
    if (!this.chartContainer?.nativeElement) {
      setTimeout(() => this.initChart(), 100);
      return;
    }

    const element = this.chartContainer.nativeElement;

    if (element.offsetWidth === 0) {
      setTimeout(() => this.initChart(), 100);
      return;
    }

    const containerWidth = element.offsetWidth || 800;
    this.width = Math.max(containerWidth - this.margin.left - this.margin.right, 600);
    this.height = 400 - this.margin.top - this.margin.bottom;

    d3.select(element).select('svg').remove();

    this.svg = d3.select(element)
      .append('svg')
      .attr('width', this.width + this.margin.left + this.margin.right)
      .attr('height', this.height + this.margin.top + this.margin.bottom)
      .append('g')
      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
  }

  private loadEmissions(): void {
    this.loading = true;
    this.error = null;

    const filters: any = {};
    if (this.selectedCountry) filters.country = this.selectedCountry;
    if (this.selectedActivity) filters.activity = this.selectedActivity;
    if (this.selectedEmissionType) filters.emission_type = this.selectedEmissionType;

    this.emissionApi.getEmissions(Object.keys(filters).length > 0 ? filters : undefined)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (emissions: Emission[]) => {
          this.emissionsData = emissions;

          if (this.availableCountries.length === 0) {
            this.updateFilterOptions(emissions);
          }

          setTimeout(() => {
            this.loading = false;
            this.cdr.detectChanges();
            
            setTimeout(() => {
              if (this.chartContainer?.nativeElement) {
                if (!this.svg) {
                  this.initChart();
                }
                this.processData(emissions);
              } else {
                setTimeout(() => {
                  if (this.chartContainer?.nativeElement) {
                    if (!this.svg) {
                      this.initChart();
                    }
                    this.processData(emissions);
                  }
                }, 200);
              }
            }, 100);
          }, 0);
        },
        error: (err) => {
          setTimeout(() => {
            this.error = 'Error loading emissions data';
            this.loading = false;
            this.cdr.detectChanges();
          }, 0);
        }
      });
  }

  private updateFilterOptions(emissions: Emission[]): void {
    this.availableCountries = Array.from(new Set(emissions.map(e => e.country))).sort();
    this.availableActivities = Array.from(new Set(emissions.map(e => e.activity))).sort();
    this.availableEmissionTypes = Array.from(new Set(emissions.map(e => e.emission_type))).sort();
  }

  public filterByCountry(country: string | null): void {
    this.selectedCountry = this.selectedCountry === country ? null : country;
    this.loadEmissions();
  }

  public filterByActivity(activity: string | null): void {
    this.selectedActivity = this.selectedActivity === activity ? null : activity;
    this.loadEmissions();
  }

  public filterByEmissionType(emissionType: string | null): void {
    this.selectedEmissionType = this.selectedEmissionType === emissionType ? null : emissionType;
    this.loadEmissions();
  }

  public clearFilters(): void {
    this.selectedCountry = null;
    this.selectedActivity = null;
    this.selectedEmissionType = null;
    this.loadEmissions();
  }

  private processData(emissions: Emission[]): void {
    if (!emissions || emissions.length === 0) {
      this.error = 'No data available';
      return;
    }

    if (!this.svg) {
      setTimeout(() => this.processData(emissions), 100);
      return;
    }

    const years = Array.from(new Set(emissions.map(e => e.year))).sort((a, b) => a - b);
    const groupedByType = d3.group(emissions, d => d.emission_type);

    const lineData: Array<{
      label: string;
      type: string;
      values: Array<{
        year: number;
        emissions: number;
      }>
    }> = [];

    groupedByType.forEach((values, type) => {
      const yearMap = new Map<number, number>();
      values.forEach(e => {
        const current = yearMap.get(e.year) || 0;
        yearMap.set(e.year, current + e.emissions);
      });

      const valuesArray = years.map(year => ({
        year,
        emissions: yearMap.get(year) || 0
      }));

      lineData.push({
        label: type,
        type: type,
        values: valuesArray
      });
    });

    this.drawChart(lineData, years);
  }

  private drawChart(
    lineData: Array<{
      label: string;
      type: string;
      values: Array<{
        year: number;
        emissions: number;
      }>
    }>,
    years: number[]
  ): void {
    if (!this.svg) {
      return;
    }

    if (!lineData || lineData.length === 0) {
      return;
    }

    this.svg.selectAll('*').remove();
    if (isPlatformBrowser(this.platformId)) {
      d3.select('.emissions-tooltip').remove();
    }

    const xScale = d3.scaleLinear()
      .domain(d3.extent(years) as [number, number])
      .range([0, this.width]);

    const maxEmissions = d3.max(lineData.flatMap(d => d.values.map(v => v.emissions))) || 0;
    const yScale = d3.scaleLinear()
      .domain([0, maxEmissions * 1.1])
      .range([this.height, 0]);

    const colors = d3.scaleOrdinal(d3.schemeCategory10);

    const line = d3.line<{ year: number; emissions: number }>()
      .x(d => xScale(d.year))
      .y(d => yScale(d.emissions))
      .curve(d3.curveMonotoneX);

    let tooltip: any = null;
    if (isPlatformBrowser(this.platformId)) {
      tooltip = d3.select('body')
        .append('div')
        .attr('class', 'emissions-tooltip')
        .style('opacity', 0)
        .style('position', 'absolute')
        .style('background-color', 'rgba(0, 0, 0, 0.8)')
        .style('color', 'white')
        .style('padding', '10px')
        .style('border-radius', '5px')
        .style('pointer-events', 'none')
        .style('font-size', '12px')
        .style('z-index', '1000');
    }

    lineData.forEach((data, index) => {
      const validValues = data.values.filter(d => d.emissions > 0);

      if (validValues.length > 0) {
        this.svg.append('path')
          .datum(validValues)
          .attr('fill', 'none')
          .attr('stroke', colors(data.type))
          .attr('stroke-width', 3)
          .attr('d', line)
          .attr('class', `line line-${index}`)
          .style('opacity', 0.9);

        this.svg.selectAll(`.dot-${index}`)
          .data(validValues)
          .enter()
          .append('circle')
          .attr('class', `dot dot-${index}`)
          .attr('cx', (d: { year: number; emissions: number }) => xScale(d.year))
          .attr('cy', (d: { year: number; emissions: number }) => yScale(d.emissions))
          .attr('r', 6)
          .attr('fill', colors(data.type))
          .attr('stroke', '#fff')
          .attr('stroke-width', 2)
          .style('cursor', 'pointer')
          .on('mouseover', function(this: SVGCircleElement, event: MouseEvent, d: { year: number; emissions: number }) {
            d3.select(this).attr('r', 8);

            if (tooltip) {
              let tooltipContent = `<strong>Type: ${data.type}</strong><br/>`;
              tooltipContent += `Year: ${d.year}<br/>`;
              tooltipContent += `Emissions: ${d.emissions.toFixed(2)} tons`;

              tooltip
                .html(tooltipContent)
                .style('opacity', 1)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 10) + 'px');
            }
          })
          .on('mouseout', function(this: SVGCircleElement) {
            d3.select(this).attr('r', 6);
            if (tooltip) {
              tooltip.style('opacity', 0);
            }
          });
      }
    });

    const xAxis = d3.axisBottom(xScale)
      .tickValues(years)
      .tickFormat(d => d3.format('d')(d as number));

    const yAxis = d3.axisLeft(yScale)
      .tickFormat(d => d3.format('.1f')(d as number));

    const xAxisGroup = this.svg.append('g')
      .attr('transform', `translate(0,${this.height})`)
      .call(xAxis);

    xAxisGroup.selectAll('text')
      .style('text-anchor', 'middle')
      .style('font-size', '13px')
      .style('font-weight', '500');

    xAxisGroup.append('text')
      .attr('x', this.width / 2)
      .attr('y', 50)
      .attr('fill', 'currentColor')
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .text('Year');

    this.svg.append('g')
      .call(yAxis)
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -60)
      .attr('x', -this.height / 2)
      .attr('fill', 'currentColor')
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .text('Emissions (tons)');

    this.svg.append('text')
      .attr('x', this.width / 2)
      .attr('y', -10)
      .attr('fill', 'currentColor')
      .style('text-anchor', 'middle')
      .style('font-size', '18px')
      .style('font-weight', 'bold')
      .text('Greenhouse Gas Emissions by Year');
  }
}
