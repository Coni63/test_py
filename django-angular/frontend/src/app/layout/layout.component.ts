import { Component } from '@angular/core';
import { TrafficLightComponent } from '../traffic-light/traffic-light.component';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [TrafficLightComponent],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss'
})
export class LayoutComponent {
  visible: boolean = true;
  expanded: boolean = false;

  toggle_sidebar() {
    this.visible = !this.visible;
  }

  test(event: any){
    event.stopPropagation();
    this.expanded = !this.expanded;
  }

  toogleTeam(event: any, team: string){
    event.stopPropagation();
    console.log(team);
  }

  logout(event: any){
    event.stopPropagation();

  }
}
