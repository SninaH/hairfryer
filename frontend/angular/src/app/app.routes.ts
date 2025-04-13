import { Routes } from '@angular/router';
import { MainPageComponent } from './components/main-page/main-page.component';
import { AnnotateComponent } from './components/annotate/annotate.component';
import { ReportComponent } from './components/report/report.component';
import { CoachComponent } from './components/coach/coach.component';

export const routes: Routes = [
    { path: '', component: MainPageComponent }, // Redirect to main page where you insert the link
    { path: 'annotate', component: AnnotateComponent }, // Redirect to annotation page
    { path: 'report', component: ReportComponent }, // Redirect to report page
    { path: 'coach', component: CoachComponent }, // Redirect to coach page
];
