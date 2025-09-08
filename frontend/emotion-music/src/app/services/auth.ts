import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  login(email: string, password: string): boolean {
    if (email && password) {
      localStorage.setItem('token', 'fake-jwt-token');
      return true;
    }
    return false;
  }

  logout(): void {
    localStorage.removeItem('token');
  }
}
