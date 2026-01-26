import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimpleSignupComponent } from './simple-signup.component';

describe('SimpleSignupComponent', () => {
  let component: SimpleSignupComponent;
  let fixture: ComponentFixture<SimpleSignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SimpleSignupComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SimpleSignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
