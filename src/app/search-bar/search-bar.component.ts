import { Component } from '@angular/core';
import { SearchService } from '../search.service'; // Adjust the path as necessary
import { SaveProductService } from '../save-product.service';
import { HeaderComponent } from '../header/header.component';
import { ActivatedRoute, Router } from '@angular/router';
import { SharedDataService } from '../shared-data.service';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent {
  products: any[] = [];

  constructor(
    private saveProductService: SaveProductService,
    private route: ActivatedRoute,
    private sharedDataService: SharedDataService,
    private router: Router ,// Inject the Router for navigation
    private searchService: SearchService
  ) {}

  searchQuery: string = '';

  onSearch(query: string) {
    this.searchQuery = query;
    console.log('Search query:', this.searchQuery);
    // You can add more search logic here
  }


  
 // submitSearch() {
 //   //console.log('Submit search for:', this.searchQuery);
 //   console.log('searching...')
 //   this.searchService.setQuery(this.searchQuery)
 // }

 submitSearch() {
  this.searchService.setQuery(this.searchQuery);
  this.router.navigate(['/results'], { queryParams: { search: this.searchQuery } });
}

}