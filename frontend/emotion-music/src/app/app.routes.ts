import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login';
import { EmotionComponent } from './pages/emotion/emotion';
import { RecommendationsComponent } from './pages/recommendations/recommendations';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'emotion', component: EmotionComponent },
  { path: 'recommendations', component: RecommendationsComponent },
];
