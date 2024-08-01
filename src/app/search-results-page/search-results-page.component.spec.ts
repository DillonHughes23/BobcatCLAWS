import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { of } from 'rxjs';

import { SearchResultsPageComponent } from './search-results-page.component';
import { SearchService } from '../search.service';
import { SaveProductService } from '../save-product.service';
import { SharedDataService } from '../shared-data.service';

describe('SearchResultsPageComponent', () => {
  let component: SearchResultsPageComponent;
  let fixture: ComponentFixture<SearchResultsPageComponent>;
  let mockSearchService: any;
  let mockSaveProductService: any;
  let mockSharedDataService: any;
  let mockRouter: any;

  beforeEach(async () => {
    mockSearchService = jasmine.createSpyObj('SearchService', ['query$']);
    mockSearchService.query$ = of('testQuery');
    mockSaveProductService = jasmine.createSpyObj('SaveProductService', ['getProductsByCategory']);
    mockSharedDataService = jasmine.createSpyObj('SharedDataService', ['selectProduct', 'changeProducts']);
    mockRouter = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      declarations: [ SearchResultsPageComponent ],
      imports: [ RouterTestingModule ],
      providers: [
        { provide: SearchService, useValue: mockSearchService },
        { provide: SaveProductService, useValue: mockSaveProductService },
        { provide: SharedDataService, useValue: mockSharedDataService },
        { provide: Router, useValue: mockRouter }
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchResultsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should subscribe to search query on init and call searchForQuery', () => {
    spyOn(component, 'searchForQuery');
    expect(component.search).toBe('testQuery');
    expect(component.searchForQuery).toHaveBeenCalled();
  });

  it('should navigate to product page on onProductClick', () => {
    const testIndex = 1;
    component.onProductClick(testIndex);
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/productspage', testIndex]);
  });  

  it('should call getProductsByCategory with correct parameters on searchForQuery', () => {
    component.search = 'testSearch';
    component.searchForQuery();
    expect(mockSaveProductService.getProductsByCategory).toHaveBeenCalledWith('testSearch', 'Search_Products');
  });

  it('should update products on searchForQuery', () => {
    const testProducts = [{id: 1, name: 'Product 1'}, {id: 2, name: 'Product 2'}];
    mockSaveProductService.getProductsByCategory.and.returnValue(of(testProducts));
    component.search = 'testSearch';
    component.searchForQuery();
    expect(component.products).toEqual(testProducts);
  });

  describe('Sorting Functionality', () => {
    beforeEach(() => {
      component.products = [
        { Product_Price: 10 },
        { Product_Price: 20 },
        { Product_Price: 15 }
      ];
    });

    it('should sort products high to low on sortHighToLow', () => {
      component.onSortChange('highToLow');
      expect(component.products[0].Product_Price).toBe(20);
      expect(component.products[1].Product_Price).toBe(15);
      expect(component.products[2].Product_Price).toBe(10);
    });

    it('should sort products low to high on sortLowToHigh', () => {
      component.onSortChange('lowToHigh');
      expect(component.products[0].Product_Price).toBe(10);
      expect(component.products[1].Product_Price).toBe(15);
      expect(component.products[2].Product_Price).toBe(20);
    });
  });

  // Add more tests as needed to cover different scenarios and logic paths
});
