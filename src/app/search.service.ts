import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private data: any[] = []; // This should be your products data
  private searchResultsSource = new BehaviorSubject<any[]>([]);
  searchResults$ = this.searchResultsSource.asObservable();
  private querySource = new BehaviorSubject<string>('');
  query$ = this.querySource.asObservable();

  constructor(private http: HttpClient) {
    // If you need to load data initially, do it here
    //this.loadData();
  }

  /* private loadData(): void {
    this.http.get<any[]>('assets/db_data.json').subscribe(data => {
      this.data = data;
    });
  }
  */

  setQuery(value: string) {
    console.log('Setting query:', value);
    this.querySource.next(value);
    this.search(value); // Call search method when query is set
  }

  getQuery() {
    return this.querySource.getValue();
  }

  search(query: string): void {
    if (!query.trim()) {
      this.searchResultsSource.next([]);
    } else {
      const filteredResults = this.data.filter(item => 
        item.name.toLowerCase().includes(query.toLowerCase()) ||
        item.category.toLowerCase().includes(query.toLowerCase())
      );
      this.searchResultsSource.next(filteredResults);
    }
  }

  // Other methods...
}
