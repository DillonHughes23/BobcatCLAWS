import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatDividerModule } from '@angular/material/divider';
import { SearchBarComponent } from './search-bar/search-bar.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatListModule } from '@angular/material/list';
import { HeaderComponent } from './header/header.component';
import { MatSliderModule } from '@angular/material/slider';
import { HttpClientModule } from '@angular/common/http';


import { HomepageComponent } from './homepage/homepage.component';
import { CategoryPageComponent } from './category-page/category-page.component';
import { ProductDetailsComponent } from './product-page/product-page.component';
import { SearchResultsPageComponent } from './search-results-page/search-results-page.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { PriceFilterComponent } from './price-filter/price-filter.component';


@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    CategoryPageComponent,
    SearchBarComponent,
    HeaderComponent,
    ProductDetailsComponent,
    SearchResultsPageComponent,
    AboutUsComponent,
    PriceFilterComponent,
    // This should match the exported class name in your component file
    // ... any other components ...
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,
    MatFormFieldModule,
    MatInputModule,
    MatGridListModule,
    MatDividerModule,
    MatPaginatorModule,
    MatListModule,
    MatSliderModule,
    // ... any other modules ...
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
