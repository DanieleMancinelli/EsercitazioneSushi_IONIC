import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StaffService } from './services/staff';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent implements OnInit {
  orders: any[] = [];
  products: any[] = [];
  categories: any[] = [];
  newProduct: any = { name: '', price: 0, image_url: '', category_id: 1 };

  constructor(private staffService: StaffService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.refreshData();
  }

  refreshData() {
    this.staffService.getOrders().subscribe(d => { this.orders = d; this.cdr.detectChanges(); });
    this.staffService.getMenu().subscribe(d => {
      this.products = d.products;
      this.categories = d.categories;
      this.cdr.detectChanges();
    });
  }

  submitProduct() {
    this.staffService.saveProduct(this.newProduct).subscribe(() => {
      alert("Operazione completata!");
      this.newProduct = { name: '', price: 0, image_url: '', category_id: 1 };
      this.refreshData();
    });
  }

  editProduct(p: any) { this.newProduct = { ...p }; }

  changeStatus(id: number, status: string) {
    this.staffService.updateStatus(id, status).subscribe(() => this.refreshData());
  }

  deleteItem(id: number) {
    if(confirm("Eliminare?")) this.staffService.deleteProduct(id).subscribe(() => this.refreshData());
  }
}