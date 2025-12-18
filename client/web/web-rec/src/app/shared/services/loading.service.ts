import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {

  private loadingSubject = new BehaviorSubject<boolean>(false);

  private isLoading$ = this.loadingSubject.asObservable();

  show(): void{
    this.loadingSubject.next(true);
  }

  hide(): void{
    this.loadingSubject.next(false);
  }

  toggle(): void{
    this.loadingSubject.next(!this.loadingSubject.value);
  }

  constructor() { }
}
