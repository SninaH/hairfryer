import { Routes } from '@angular/router';
import { MainPageComponent } from './components/main-page/main-page.component';
import { AnnotateComponent } from './components/annotate/annotate.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent }, // Redirect to main page where you insert the link
    { path: 'annotate', component: AnnotateComponent }, // Redirect to annotation page
];
