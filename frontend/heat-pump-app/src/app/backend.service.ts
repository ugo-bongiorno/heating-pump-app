import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from './../environments/environment';
import { CurrentWaterTemperature, CurrentTargetTemperature } from '../interfaces/response-interfaces';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private http: HttpClient) { }

  getCurrentWaterTemp(): Promise<CurrentWaterTemperature> {
    return new Promise((resolve, reject) => {
      this.http.get<CurrentWaterTemperature>(environment.backend_url + '/get_water_temperature').subscribe(
        (response)=>{resolve(response);},
        (error)=> {reject(error);}
      )
    });
  };

  getTargetWaterTemp(): Promise<CurrentTargetTemperature> {
    return new Promise((resolve, reject) => {
      this.http.get<CurrentTargetTemperature>(environment.backend_url + '/get_target_water_temperature').subscribe(
          (response)=>{resolve(response);},
          (error)=> {reject(error);}
        )
      });
    };

  setTargetWaterTemp(targetTemperature: number): Promise<CurrentTargetTemperature> {
    return new Promise((resolve, reject) => {
      this.http.post<CurrentTargetTemperature>(
        environment.backend_url + '/set_target_water_temperature',
        {'target_water_temperature': targetTemperature}
      ).subscribe(
          (response)=>{resolve(response);},
          (error)=> {reject(error);}
        )
      });
    };
}
