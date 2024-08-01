import { Component, OnInit } from '@angular/core';
import { SharedDataService } from '../shared-data.service';

@Component({
  selector: 'app-product-page',
  templateUrl: './product-page.component.html',
  styleUrls: ['./product-page.component.css']
})
export class ProductDetailsComponent implements OnInit {
  selectedProduct: any;
  otherProducts: any[] = []; // Array for the rest of the products

  constructor(
    private sharedDataService: SharedDataService
  ) {}

  ngOnInit(): void {
    this.sharedDataService.currentSelectedIndex.subscribe(index => {
      if (index !== null) {
        this.sharedDataService.currentProducts.subscribe(products => {
          if (index >= 0 && index < products.length) {
            this.selectedProduct = products[index];
            this.otherProducts = products.filter((_, i) => i !== index);
          }
        });
      }
    });
  }

  onProductSelect(product: any) {
    this.selectedProduct = product;
    this.otherProducts = this.otherProducts.filter(p => p !== product);
  }
}
