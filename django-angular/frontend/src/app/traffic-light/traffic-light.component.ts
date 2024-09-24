import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-traffic-light',
  standalone: true,
  imports: [],
  templateUrl: './traffic-light.component.html',
  styleUrl: './traffic-light.component.scss'
})
export class TrafficLightComponent {
  @Input() set status(status: string) {
    if (status == "DONE") {
      this.red = false;
      this.yellow = false;
      this.green = true;
    } else if (status == "TO_REVIEW") {
      this.red = false;
      this.yellow = true;
      this.green = false;
    } else {
      this.red = true;
      this.yellow = false;
      this.green = false;
    }
  }

  green: boolean = false;
  yellow: boolean = false;
  red: boolean = false;



  // changeColor() {
  //   this.btnText = 'Next'
  //   this.count++;
  //   if (this.count == 4)
  //     this.count = 1;
  //   if (this.count == 1){
  //     this.red = 'dark light'
  //     this.green = 'green light'
  //   }
  //   else if (this.count == 2){
  //     this.orange = 'orange light'
  //     this.green = 'dark light'
  //   }
  //   else{
  //     this.red = 'red light'
  //     this.orange = 'dark light'
  //   }
  // }
}