import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedDataService {
  private productsSource = new BehaviorSubject<any[]>([]);
  private selectedProductIndex = new BehaviorSubject<number | null>(null);

  currentProducts = this.productsSource.asObservable();
  currentSelectedIndex = this.selectedProductIndex.asObservable();

  constructor() { }

  changeProducts(products: any[]) {
    this.productsSource.next(products);
  }

  selectProduct(index: number | null) {
    this.selectedProductIndex.next(index);
  }
}
