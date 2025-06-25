import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommentsComponent } from "./comments/comments.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommentsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'test_angular';
}
