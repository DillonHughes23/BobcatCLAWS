import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router'; // Import Router
import { SearchBarComponent } from './search-bar.component';
import { SearchService } from '../search.service';
import { SaveProductService } from '../save-product.service';
import { SharedDataService } from '../shared-data.service';

describe('SearchBarComponent', () => {
  let component: SearchBarComponent;
  let fixture: ComponentFixture<SearchBarComponent>;
  let mockSearchService: any;
  let mockRouter: any;

  beforeEach(async () => {
    mockSearchService = jasmine.createSpyObj('SearchService', ['setQuery']);
    mockRouter = jasmine.createSpyObj('Router', ['navigate']);

    await TestBed.configureTestingModule({
      declarations: [ SearchBarComponent ],
      imports: [ RouterTestingModule ],
      providers: [
        { provide: SearchService, useValue: mockSearchService },
        SaveProductService, // Assuming no methods of SaveProductService are called directly in the component
        SharedDataService, // Assuming no methods of SharedDataService are called directly in the component
        { provide: Router, useValue: mockRouter }
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should update searchQuery on onSearch', () => {
    const testQuery = 'test query';
    component.onSearch(testQuery);
    expect(component.searchQuery).toBe(testQuery);
  });

  it('should call setQuery on SearchService and navigate on submitSearch', () => {
    const testQuery = 'test query';
    component.searchQuery = testQuery;
    component.submitSearch();
    expect(mockSearchService.setQuery).toHaveBeenCalledWith(testQuery);
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/results'], { queryParams: { search: testQuery } });
  });

  // Add more tests as needed to cover different scenarios and logic paths
});
