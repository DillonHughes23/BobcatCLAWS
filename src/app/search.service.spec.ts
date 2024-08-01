import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SearchService } from './search.service';

describe('SearchService', () => {
  let service: SearchService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SearchService]
    });

    service = TestBed.inject(SearchService);
    // Mock data initialization if necessary
    service['data'] = [
      { name: 'Product 1', category: 'Category 1' },
      { name: 'Product 2', category: 'Category 2' }
      // Add more mock data as needed
    ];
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should set and get query', () => {
    const testQuery = 'test';
    service.setQuery(testQuery);
    expect(service.getQuery()).toBe(testQuery);
  });

  it('should filter search results based on query', () => {
    const testQuery = 'Product 1';
    service.setQuery(testQuery);

    service.searchResults$.subscribe(results => {
      expect(results.length).toBe(1);
      expect(results[0].name).toBe('Product 1');
    });
  });

  it('should return empty array for empty or whitespace query', () => {
    const testQuery = ' ';
    service.setQuery(testQuery);

    service.searchResults$.subscribe(results => {
      expect(results.length).toBe(0);
    });
  });

  // Add more tests to cover other methods and scenarios as needed
});
