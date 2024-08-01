import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-price-filter',
  templateUrl: './price-filter.component.html',
  styleUrls: ['./price-filter.component.css']
})
export class PriceFilterComponent {
  @Output() sortChange = new EventEmitter<string>();

  sortHighToLow() {
    this.sortChange.emit('highToLow');
  }

  sortLowToHigh() {
    this.sortChange.emit('lowToHigh');
  }
}
