import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SidebarService {

  private isExpandedSubject = new BehaviorSubject<boolean>(true);
  isExpanded$ = this.isExpandedSubject.asObservable();

  private isMobileOpenSubject = new BehaviorSubject<boolean>(false);
  isMobileOpen$ = this.isMobileOpenSubject.asObservable();

  private isHoveredSubject = new BehaviorSubject<boolean>(false);
  isHovered$ = this.isHoveredSubject.asObservable();

  setExpanded(val: boolean): void {
    this.isExpandedSubject.next(val);
  }

  toggleExpanded(): void {
    this.isExpandedSubject.next(!this.isExpandedSubject.value);
  }

  setMobileOpen(val: boolean): void {
    this.isMobileOpenSubject.next(val);
  }

  setHovered(val: boolean): void {
    this.isHoveredSubject.next(val);
  }

  constructor() { }
}
