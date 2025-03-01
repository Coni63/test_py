import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatapointComponent } from './datapoint.component';

describe('DatapointComponent', () => {
  let component: DatapointComponent;
  let fixture: ComponentFixture<DatapointComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatapointComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DatapointComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
