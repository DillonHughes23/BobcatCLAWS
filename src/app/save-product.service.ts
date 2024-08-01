import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SaveProductService {
  private productValue: any;
  private productCategory: any;
  private keyword: any;
  private apiUrl = 'http://localhost:3010/api'; // Update to use the correct port

  constructor(private http: HttpClient) { }

  // Fetches products by category ID from the backend
  getProductsByCategory(catId: any, proc_name:any): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/${proc_name}/${catId}`);
  }

  // Existing functionality to save and get product details
  saveProductService(value: any){
    this.productValue = value;
  }

  saveKeyword(value: any){
    this.keyword = value;
  }

  getKeyword(){
    return this.keyword;
  }

  saveCatService(value: any){
    this.productCategory = value;
    console.log('cat', this.productCategory);
  }

  getCat(){
    return this.productCategory;
  }

  getProduct(){
    console.log('value', this.productValue);
    return this.productValue;
  }

  // New functionality to fetch products by category ID from the backend
  //getProductsByCategory(catId: number): Observable<any> {
  //  return this.http.get(`http://localhost:58583/api/categories/${catId}`);
  //}

}
