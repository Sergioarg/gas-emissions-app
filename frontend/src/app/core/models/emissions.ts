export interface Emission {
    year: number;
    emissions: number;
    emission_type: string; // considerar enum de tipos de emisiones
    country: string;
    activity: string;
  }
