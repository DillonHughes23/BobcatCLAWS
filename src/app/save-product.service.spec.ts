import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SaveProductService } from './save-product.service';

describe('SaveProductService', () => {
  let service: SaveProductService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SaveProductService]
    });

    service = TestBed.inject(SaveProductService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify(); // Verify that no unmatched requests are outstanding.
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('getProductsByCategory should make GET request', () => {
    const catId = 1;
    const procName = 'procName';
    const mockProducts = [{ id: 1, name: 'Product 1' }, { id: 2, name: 'Product 2' }];

    service.getProductsByCategory(catId, procName).subscribe(products => {
      expect(products).toEqual(mockProducts);
    });

    const req = httpTestingController.expectOne(`http://localhost:3010/api/${procName}/${catId}`);
    expect(req.request.method).toEqual('GET');
    req.flush(mockProducts);
  });

  // Tests for saveProductService, saveKeyword, getKeyword, saveCatService, getCat, getProduct

  it('saveProductService should save product value', () => {
    const testValue = { id: 1, name: 'Test Product' };
    service.saveProductService(testValue);
    expect(service.getProduct()).toEqual(testValue);
  });

  // Similar tests for saveKeyword, getKeyword, saveCatService, getCat
});
