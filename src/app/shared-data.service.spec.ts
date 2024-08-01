import { TestBed } from '@angular/core/testing';
import { SharedDataService } from './shared-data.service';

describe('SharedDataService', () => {
  let service: SharedDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SharedDataService]
    });

    service = TestBed.inject(SharedDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should emit new products when changeProducts is called', () => {
    const testProducts = [{ id: 1, name: 'Product 1' }, { id: 2, name: 'Product 2' }];
    service.changeProducts(testProducts);

    service.currentProducts.subscribe(products => {
      expect(products).toEqual(testProducts);
    });
  });

  it('should emit new selected index when selectProduct is called', () => {
    const testIndex = 1;
    service.selectProduct(testIndex);

    service.currentSelectedIndex.subscribe(index => {
      expect(index).toBe(testIndex);
    });
  });

  it('should allow null as a valid product index', () => {
    service.selectProduct(null);

    service.currentSelectedIndex.subscribe(index => {
      expect(index).toBeNull();
    });
  });

  // Add more tests to cover other methods and scenarios as needed
});
