import { Component, Input, OnInit } from '@angular/core';
import { LucideAngularModule} from 'lucide-angular';

@Component({
  standalone: true,
  selector: 'app-snackbar',
  imports: [
    LucideAngularModule
  ],
  templateUrl: './snackbar.component.html',
  styleUrl: './snackbar.component.scss'
})
export class SnackbarComponent implements OnInit {

  public iconPath: string = 'M5 11.917 9.724 16.5 19 7.5';
  ngOnInit(): void {
    this.iconPath = this.makeIcon();
  }
  @Input() message: string = '';

  @Input() type: 'success' | 'error' | 'info' | "warning" = 'info';

  makeIcon(): string {
    switch (this.type) {
      case 'success': return 'M5 11.917 9.724 16.5 19 7.5';
      case 'error': return 'M6 18 17.94 6M18 18 6.06 6';
      case 'info': return 'm12 18-7 3 7-18 7 18-7-3Zm0 0v-5';
      case 'warning': return 'M12 13V8m0 8h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z';
      default: return 'm12 18-7 3 7-18 7 18-7-3Zm0 0v-5';

    }
  }
}
