import { Component, Input } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-user-avatar',
  imports: [MatTooltipModule],
  templateUrl: './user-avatar.component.html',
  styleUrl: './user-avatar.component.scss'
})
export class UserAvatarComponent {
  @Input() fullName: string = '';
  @Input() backgroundColor: string = '';

  get initials(): string {
    if (!this.fullName) return '';
    
    // Split the full name and get the first letters
    const names = this.fullName.split(' ');
    const firstInitial = names[0][0].toUpperCase();
    const lastInitial = names.length > 1 
      ? names[names.length - 1][0].toUpperCase() 
      : '';
    
    return `${firstInitial}${lastInitial}`;
  }

  // Optional: Generate a consistent color based on the name
  generateColor(name: string): string {
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    const hue = hash % 360;
    return `hsl(${hue}, 70%, 50%)`;
  }

  ngOnInit() {
    // If no background color is provided, generate one
    if (!this.backgroundColor && this.fullName) {
      this.backgroundColor = this.generateColor(this.fullName);
    }
  }
}