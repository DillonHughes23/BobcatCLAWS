import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

import { HomepageComponent } from './homepage.component';
import { SaveProductService } from '../save-product.service';
import { SharedDataService } from '../shared-data.service';

describe('HomepageComponent', () => {
  let component: HomepageComponent;
  let fixture: ComponentFixture<HomepageComponent>;
  let mockSaveProductService: any;
  let mockSharedDataService: any;
  let mockActivatedRoute: any;

  beforeEach(async () => {
    mockSaveProductService = jasmine.createSpyObj(['getProductsByCategory']);
    mockSharedDataService = jasmine.createSpyObj(['selectProduct', 'changeProducts']);
    mockActivatedRoute = {
      params: of({}) // Mock params as needed
    };

    await TestBed.configureTestingModule({
      declarations: [ HomepageComponent ],
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
    fixture = TestBed.createComponent(HomepageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Here you can add more tests to check the functionality of your component
  // For example, you could test the ngOnInit behavior, the onProductClick method, and the interaction with SaveProductService
});
