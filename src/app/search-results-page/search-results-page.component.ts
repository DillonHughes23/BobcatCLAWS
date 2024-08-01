import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search.service';
import { SharedDataService } from '../shared-data.service';
import { ActivatedRoute, Router } from '@angular/router';
import { SaveProductService } from '../save-product.service';

@Component({
  selector: 'app-search-results-page',
  templateUrl: './search-results-page.component.html',
  styleUrls: ['./search-results-page.component.css']
})
export class SearchResultsPageComponent implements OnInit {
  products: any[] = []; // Ensure this is an array
  search: any;

  constructor(
    private searchService: SearchService,
    private saveProductService: SaveProductService,
    private sharedDataService: SharedDataService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.searchService.query$.subscribe(newQuery => {
      this.search = newQuery;
      this.searchForQuery();
    });
  }
  

  onProductClick(index: number) {
    this.sharedDataService.selectProduct(index);
    this.router.navigate(['/productspage', index]);
  }

  searchForQuery() {
    this.saveProductService.getProductsByCategory(this.search, 'Search_Products').subscribe(data => {
      this.products = data;
      this.sharedDataService.changeProducts(data);
    }, error => {
      console.error('Error fetching products:', error);
    });
  }

  onSortChange(sortOrder: string) {
    if (sortOrder === 'highToLow') {
      this.sortProductsHighToLow();
    } else if (sortOrder === 'lowToHigh') {
      this.sortProductsLowToHigh();
    }
  }

  private sortProductsHighToLow() {
    this.products.sort((a, b) => b.Product_Price - a.Product_Price);
  }

  private sortProductsLowToHigh() {
    this.products.sort((a, b) => a.Product_Price - b.Product_Price);
  }

}
