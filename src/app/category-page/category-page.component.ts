import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SaveProductService } from '../save-product.service';
import { SharedDataService } from '../shared-data.service';

@Component({
  selector: 'app-category-page',
  templateUrl: './category-page.component.html',
  styleUrls: ['./category-page.component.css']
})
export class CategoryPageComponent implements OnInit {
  products: any[] = [];

  constructor(
    private saveProductService: SaveProductService,
    private route: ActivatedRoute,
    private sharedDataService: SharedDataService,
    private router: Router // Inject the Router for navigation
  ) {}

  onProductClick(index: number) {
    this.sharedDataService.selectProduct(index);
    // Navigate to the product details page with the product index
    this.router.navigate(['/productspage', index]);
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const catId = +params['id'];
      const proc_db = 'Get_20_by_subcat'
      if (!isNaN(catId)) {
        this.saveProductService.getProductsByCategory(catId, proc_db).subscribe(data => {
          this.products = data;
          this.sharedDataService.changeProducts(data);
        }, error => {
          console.error('Error fetching products:', error);
        });
      } else {
        console.error(`The category ID is not a valid number.`);
      }
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
