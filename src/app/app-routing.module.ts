import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';
import { CategoryPageComponent } from './category-page/category-page.component';
import { ProductDetailsComponent } from './product-page/product-page.component';
import { SearchResultsPageComponent } from './search-results-page/search-results-page.component';
import { AboutUsComponent } from './about-us/about-us.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomepageComponent },
  { path: 'categories/:id', component: CategoryPageComponent },
  { path: 'productspage/:id', component: ProductDetailsComponent },
  { path: 'results', component: SearchResultsPageComponent},
  { path: 'about-us', component: AboutUsComponent },



  // path: 'productspage/:id', component: ProductsPageComponent },

  // Add a route parameter for category IDs
  // If you have specific categories, you may have other routes for them or use query parameters instead
  // If you want to catch all other paths that are not defined, you can use a wildcard route
  //{ path: '**', component: PageNotFoundComponent }, // PageNotFoundComponent needs to be created
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
