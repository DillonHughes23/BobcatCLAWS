import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PriceFilterComponent } from './price-filter.component';

describe('PriceFilterComponent', () => {
  let component: PriceFilterComponent;
  let fixture: ComponentFixture<PriceFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PriceFilterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PriceFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should emit "highToLow" when sortHighToLow is called', () => {
    spyOn(component.sortChange, 'emit');

    component.sortHighToLow();

    expect(component.sortChange.emit).toHaveBeenCalledWith('highToLow');
  });

  it('should emit "lowToHigh" when sortLowToHigh is called', () => {
    spyOn(component.sortChange, 'emit');

    component.sortLowToHigh();

    expect(component.sortChange.emit).toHaveBeenCalledWith('lowToHigh');
  });
});
