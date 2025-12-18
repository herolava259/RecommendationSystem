import { Component, ElementRef, HostListener, ViewChild } from '@angular/core';
import { DatePipe } from '@angular/common'; 

@Component({
  selector: 'app-footer',
  imports: [DatePipe],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss'
})
export class FooterComponent {

  now = new Date();

  @ViewChild("orbRef") orbRef!: ElementRef<HTMLDivElement> ;

  @HostListener('document:mousemove', ['$event'])
  onMouseMove(event: MouseEvent)
  {
    const orb = this.orbRef.nativeElement;
    orb.style.left = `${event.clientX}px`;
    orb.style.top = `${event.clientY}px`;
  }

}
