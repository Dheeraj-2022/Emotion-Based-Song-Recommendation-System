import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login';
import { RegisterComponent } from './pages/register/register';
import { EmotionComponent } from './pages/emotion/emotion';
import { RecommendationsComponent } from './pages/recommendations/recommendations';

export const routes: Routes = [
  { path: '', redirectTo: 'register', pathMatch: 'full' },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'emotion', component: EmotionComponent },
  { path: 'recommendations', component: RecommendationsComponent },
];
