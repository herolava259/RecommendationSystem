import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'safeHtml'
})
export class SafeHtmlPipe implements PipeTransform {

  // eslint-disable-next-line @angular-eslint/prefer-inject
  constructor(private sanitizer: DomSanitizer) {}

  transform(value:string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(value);
  }

}
