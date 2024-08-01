import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

import { CategoryPageComponent } from './category-page.component';
import { SaveProductService } from '../save-product.service';
import { SharedDataService } from '../shared-data.service';

describe('CategoryPageComponent', () => {
  let component: CategoryPageComponent;
  let fixture: ComponentFixture<CategoryPageComponent>;
  let mockSaveProductService: any;
  let mockSharedDataService: any;
  let mockActivatedRoute: any;

  beforeEach(async () => {
    mockSaveProductService = jasmine.createSpyObj(['getProductsByCategory']);
    mockSharedDataService = jasmine.createSpyObj(['selectProduct', 'changeProducts']);
    mockActivatedRoute = {
      params: of({ id: '123' }) // Mock params with an id
    };

    await TestBed.configureTestingModule({
      declarations: [ CategoryPageComponent ],
      imports: [ RouterTestingModule ],
      providers: [
        { provide: SaveProductService, useValue: mockSaveProductService },
        { provide: SharedDataService, useValue: mockSharedDataService },
        { provide: ActivatedRoute, useValue: mockActivatedRoute }
        // Add any other dependencies here
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CategoryPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Add more tests here to test the functionality of your component
});
