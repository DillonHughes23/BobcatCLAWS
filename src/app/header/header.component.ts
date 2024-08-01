import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SaveProductService } from '../save-product.service';

interface CategoryMapping {
  [key: string]: number;
}

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  private categoryMapping: CategoryMapping = {
    'Bedding and Linens': 1,
    'Desk Supplies': 2,
    'Room Decor': 3,
    'Storage Solutions': 4,
    'Kitchen and Dining': 5,
    'Laptops and Accessories': 6,
    'Audio and Headphones': 7,
    'Gaming and Entertainment': 8,
    'Smart Home Devices': 9,
    'Cables and Adaptors': 10,
    'Mini Fridges': 11,
    'Microwaves and Cooking Appliances': 12,
    'Coffee and Tea Makers': 13,
    'Laundry and Cleaning Appliances': 14,
    'Heating and Cooling': 15,
    'Cell Phones and Accessories': 16,
  };


  constructor(private saveProductService: SaveProductService, private router: Router) {}

  /*
  onSelectSubCategory(subCategory: string) {
    const categoryId = this.mapSubCategoryToId(subCategory);
    console.log('Error cant get into onSelectSubcategory.');
    if (categoryId !== null) {
      this.saveProductService.getProductsByCategory(categoryId).subscribe(
        (data) => {
          this.saveProductService.saveCatService(data);
          this.saveProductService.saveKeyword(subCategory);
          this.router.navigate(['/categories', categoryId]);
        },
        (error) => {
          console.error('Error fetching category:', error);
        }
      );
    } else {
      console.error('Invalid subcategory selected:', subCategory);
    }
  }
    */

  private mapSubCategoryToId(subCategory: string): number | null {
    return this.categoryMapping[subCategory] || null;
  }
}
  //getSubCategories(mainCategory: string): string[] {
    // Logic to return an array of subcategory names based on main category
    // For now, we'll just return all subcategory names, but you can adjust as needed
    //return Object.keys(this.categoryMapping);
  //}
//}
