import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class StaffService {
  private apiUrl = 'https://special-guide-7vx56wj6jgx3xvw7-5000.app.github.dev'; 

  constructor(private http: HttpClient) { }

  getOrders(): Observable<any[]> { return this.http.get<any[]>(this.apiUrl + '/staff/orders'); }
  updateStatus(id: number, status: string): Observable<any> { 
    return this.http.put(this.apiUrl + '/staff/orders/' + id + '/status', { status }); 
  }
  getMenu(): Observable<any> { return this.http.get(this.apiUrl + '/menu'); }
  
  saveProduct(product: any): Observable<any> {
    if (product.id) { return this.http.put(this.apiUrl + '/staff/products/' + product.id, product); }
    return this.http.post(this.apiUrl + '/staff/products', product);
  }
  
  deleteProduct(id: number): Observable<any> { return this.http.delete(this.apiUrl + '/staff/products/' + id); }
}