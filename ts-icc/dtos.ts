/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface BrightnessRequest {
  target: string;
  operation: string;
  brightness: number;
}
export interface HsvRequest {
  target: string;
  operation: string;
  h?: number;
  s?: number;
  v?: number;
}
export interface LightingRequest {
  target: string;
  operation: string;
}
export interface TemperatureRequest {
  target: string;
  operation: string;
  temperature: string;
}
