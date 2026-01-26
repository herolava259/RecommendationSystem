import { inject, Injectable } from '@angular/core';
import { HotToastService  } from '@ngxpert/hot-toast';

@Injectable({
  providedIn: 'root'
})
export class SnackbarService {

  toast = inject(HotToastService);

  showError(message: string, delay: number = 3000) : void 
  {
    const toastRef = this.toast.error(message, {
      autoClose: false,
      theme: "snackbar",
      position: "bottom-center",
      dismissible: true,
    });

    setTimeout(() => {
      toastRef.close();
    }, delay);

    // for debug
    toastRef.afterClosed.subscribe(() => {
      console.log('Error Snackbar closed');
    });
  }

  show(message: string, delay: number = 3000) : void {
    const toastRef = this.toast.show(message, 
      {
        theme: "snackbar",
        position: "bottom-center",
        icon: "🌞",
        autoClose: false,
      }
    );

    // close 

    setTimeout(() => {
      toastRef.close();
    }, delay);

    // for debug 

    toastRef.afterClosed.subscribe(() => {
      console.log('Snackbar closed');
    });
  }

  constructor() { }
}
