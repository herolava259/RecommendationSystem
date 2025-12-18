import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ModalService {

  private isOpenSubject = new BehaviorSubject<boolean>(false);

  isOpen$: Observable<boolean> = this.isOpenSubject.asObservable();


  get isOpen(): boolean{
    return this.isOpenSubject.value;
  }

  openModal(): void {
    this.isOpenSubject.next(true);
  }

  closeModal(): void {
    this.isOpenSubject.next(false);
  }

  toggleModal(): void {
    this.isOpenSubject.next(!this.isOpenSubject.value);
  }

  constructor() { }
}
