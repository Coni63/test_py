import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-comments',
  imports: [CommonModule, FormsModule],
  templateUrl: './comments.component.html',
  styleUrl: './comments.component.scss'
})
export class CommentsComponent {
  newMessage = '';
  currentUser = 'alice42'; // À remplacer par l'utilisateur réel
  
  sendMessage() {
    if (this.newMessage.trim()) {
      this.data.push({
        message: this.newMessage,
        created_by: {
          username: this.currentUser
        },
        created_at: new Date().toISOString(),
        roles: this.currentUser === 'alice42' ? 'reviewer' : 'validator'
      });
      this.newMessage = '';
    }
  }

  data = [
  {
    message: "Salut, tu as vérifié le dernier commit ?",
    created_by: {
      username: "alice42"
    },
    created_at: "2025-06-25T08:15:23Z",
    roles: "reviewer"
  },
  {
    message: "Oui, tout semble correct.",
    created_by: {
      username: "bob_dev"
    },
    created_at: "2025-06-25T08:16:10Z",
    roles: "validator"
  },
  {
    message: "Parfait, je merge alors.",
    created_by: {
      username: "alice42"
    },
    created_at: "2025-06-25T08:16:42Z",
    roles: "reviewer"
  },
  {
    message: "Vas-y, je te laisse faire.",
    created_by: {
      username: "bob_dev"
    },
    created_at: "2025-06-25T08:17:05Z",
    roles: "validator"
  },
  {
    message: "C'est bon, c'est en prod 🚀",
    created_by: {
      username: "alice42"
    },
    created_at: "2025-06-25T08:18:01Z",
    roles: "reviewer"
  }
];

}
