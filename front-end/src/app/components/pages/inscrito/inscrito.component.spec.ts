import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InscritoComponent } from './inscrito.component';

describe('InscritoComponent', () => {
  let component: InscritoComponent;
  let fixture: ComponentFixture<InscritoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InscritoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InscritoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
