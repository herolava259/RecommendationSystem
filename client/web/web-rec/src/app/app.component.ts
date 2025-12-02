import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SignupComponent } from './account/signup/signup.component';
import { SigninComponent } from "./account/signin/signin.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, SignupComponent, SigninComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'web-rec';
}
