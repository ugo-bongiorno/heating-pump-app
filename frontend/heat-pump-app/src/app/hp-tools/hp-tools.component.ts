import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { BackendService } from '../backend.service';


@Component({
  selector: 'app-hp-tools',
  templateUrl: './hp-tools.component.html',
  styleUrls: ['./hp-tools.component.css']
})
export class HpToolsComponent implements OnInit {
  currentWaterTemperature: any = '-';
  currentTargetTemperature: any = '-';
  targetWaterTemp: FormControl;

  constructor(private backendService: BackendService) {
  }

  ngOnInit(): void {
    // build the target water temperature from control
    this.targetWaterTemp = new FormControl(null, [Validators.required, Validators.max(35), Validators.min(15)]);

    // get current water temperature
    this.refreshCurrentWaterTemp()

    // get current target temperature
    this.refreshTargetWaterTemp()
  }

  async refreshCurrentWaterTemp() {
    try{
      let response = await this.backendService.getCurrentWaterTemp();
      this.currentWaterTemperature= response.current_water_temperature;
    } catch(error) {
      console.log(error);
    }
  }

  async refreshTargetWaterTemp() {
    try {
      let response = await this.backendService.getTargetWaterTemp();
      this.currentTargetTemperature = response.target_water_temperature;
    } catch(error) {
      console.log(error);
    }
  }

  async submitTargetWaterTemp() {
    try {
      await this.backendService.setTargetWaterTemp(this.targetWaterTemp.value);
      await this.refreshTargetWaterTemp();
    } catch(error) {
      console.log(error);
    } finally {
      this.targetWaterTemp.reset();
    }
  }

}
