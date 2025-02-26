import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PdfDataViewerComponent } from './pdf-data-viewer.component';

describe('PdfDataViewerComponent', () => {
  let component: PdfDataViewerComponent;
  let fixture: ComponentFixture<PdfDataViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PdfDataViewerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PdfDataViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
