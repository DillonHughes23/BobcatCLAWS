import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HeaderComponent } from './header.component';
import { SaveProductService } from '../save-product.service';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: ComponentFixture<HeaderComponent>;
  let mockSaveProductService: any;

  beforeEach(async () => {
    // Mock SaveProductService
    mockSaveProductService = jasmine.createSpyObj(['getProductsByCategory', 'saveCatService', 'saveKeyword']);

    await TestBed.configureTestingModule({
      declarations: [ HeaderComponent ],
      imports: [ RouterTestingModule ],
      providers: [
        { provide: SaveProductService, useValue: mockSaveProductService }
        // Add any other dependencies here
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // add more tests 

});
