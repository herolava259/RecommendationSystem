import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {

  private readonly darkBgTheme = 'dark:bg-gray-900';
  private readonly darkTheme = "dark";

  private themeSubject = new BehaviorSubject<string>('light');
  theme$ = this.themeSubject.asObservable();



  constructor() {
    const newTheme = this.themeSubject.value === "light" ? "dark" : "light";

    
   }

   toggleTheme(): void {
    const newTheme = this.themeSubject.value === "light" ? "dark" : "light";
    this.themeSubject.next(newTheme);
   }

   setTheme(theme: string): void {

    this.themeSubject.next(theme);

    localStorage.setItem("app-theme", theme);

    if(theme === "dark"){
      document.documentElement.classList.add(this.darkTheme);
      document.body.classList.add(this.darkBgTheme);
    } 
    else{
      document.documentElement.classList.remove(this.darkTheme);
      document.body.classList.remove(this.darkBgTheme);
    }
   }
}
