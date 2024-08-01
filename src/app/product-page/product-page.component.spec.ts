import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { ProductDetailsComponent } from './product-page.component';
import { SharedDataService } from '../shared-data.service';

describe('ProductDetailsComponent', () => {
  let component: ProductDetailsComponent;
  let fixture: ComponentFixture<ProductDetailsComponent>;
  let mockSharedDataService: any;

  beforeEach(async () => {
    // Mock SharedDataService
    mockSharedDataService = jasmine.createSpyObj('SharedDataService', ['currentSelectedIndex', 'currentProducts']);
    
    // Mock Observables
    mockSharedDataService.currentSelectedIndex = of(0);
    mockSharedDataService.currentProducts = of([{id: 1, name: 'Product 1'}, {id: 2, name: 'Product 2'}]);

    await TestBed.configureTestingModule({
      declarations: [ ProductDetailsComponent ],
      providers: [
        { provide: SharedDataService, useValue: mockSharedDataService }
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set selectedProduct and otherProducts correctly on init', () => {
    expect(component.selectedProduct).toEqual({id: 1, name: 'Product 1'});
    expect(component.otherProducts).toEqual([{id: 2, name: 'Product 2'}]);
  });

  it('should update selectedProduct and otherProducts on onProductSelect', () => {
    const newProduct = {id: 3, name: 'Product 3'};
    component.onProductSelect(newProduct);
    expect(component.selectedProduct).toEqual(newProduct);
    // Expect otherProducts to not include newProduct, adjust as per your logic
    expect(component.otherProducts).not.toContain(newProduct);
  });

  // Add more tests as needed to cover different scenarios and logic paths
});
