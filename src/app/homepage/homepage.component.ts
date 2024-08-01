import { Component, OnInit } from '@angular/core';
import { SaveProductService } from '../save-product.service';
import { HeaderComponent } from '../header/header.component';
import { ActivatedRoute, Router } from '@angular/router';
import { SharedDataService } from '../shared-data.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  
  products: any[] = [];

  constructor(
    private saveProductService: SaveProductService,
    private route: ActivatedRoute,
    private sharedDataService: SharedDataService,
    private router: Router // Inject the Router for navigation
  ) {}

 ngOnInit(): void {
  this.route.params.subscribe(params => {
    const limit = 25;
    const proc_db = 'Get_Homepage_Products'
    if (!isNaN(limit)) {
      this.saveProductService.getProductsByCategory(limit, proc_db).subscribe(data => {
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
onProductClick(index: number) {
  this.sharedDataService.selectProduct(index);
  // Navigate to the product details page with the product index
  this.router.navigate(['/productspage', index]);
}
    // Sub cat selection
    
}
