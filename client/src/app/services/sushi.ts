import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SushiService {
  // Incolla qui l'URL della tua porta 5000 (Flask)
  private apiUrl = 'https://special-guide-7vx56wj6jgx3xvw7-5000.app.github.dev';

  constructor(private http: HttpClient) { }

  getMenu(): Observable<any> {
    return this.http.get(`${this.apiUrl}/menu`);
  }

  sendOrder(order: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/orders`, order);
  }

  getOrderStatus(table: string, user: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders/status?table=${table}&user=${user}`);
  }
}