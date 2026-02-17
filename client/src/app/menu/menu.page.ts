import { Component, OnInit, OnDestroy } from '@angular/core';
import { IonicModule, ToastController } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SushiService } from '../services/sushi';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.page.html',
  styleUrls: ['./menu.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class MenuPage implements OnInit, OnDestroy {
  products: any[] = [];
  categories: any[] = [];
  cart: any[] = [];
  userOrders: any[] = [];
  refreshInterval: any;
  
  table: string = localStorage.getItem('table') || '';
  user: string = localStorage.getItem('user') || '';

  constructor(private sushiService: SushiService, private toastCtrl: ToastController) {}

  ngOnInit() {
    this.sushiService.getMenu().subscribe(data => {
      this.products = data.products;
      this.categories = data.categories;
    });
    this.refreshStatus();
    // AUTO-REFRESH dello stato ogni 5 secondi
    this.refreshInterval = setInterval(() => { this.refreshStatus(); }, 5000);
  }

  ngOnDestroy() {
    if (this.refreshInterval) clearInterval(this.refreshInterval);
  }

  refreshStatus() {
    this.sushiService.getOrderStatus(this.table, this.user).subscribe(data => { this.userOrders = data; });
  }

  addToCart(product: any) {
    const existing = this.cart.find(item => item.id === product.id);
    if (existing) { existing.qty++; } 
    else { this.cart.push({ id: product.id, name: product.name, qty: 1, price: product.price }); }
  }

  async sendOrder() {
    if (this.cart.length === 0) return;
    this.sushiService.sendOrder({ table: this.table, user: this.user, items: this.cart }).subscribe(async () => {
      const toast = await this.toastCtrl.create({ message: 'Ordine inviato!', duration: 2000, color: 'success' });
      toast.present();
      this.cart = [];
      this.refreshStatus();
    });
  }

  getProductsByCategory(catId: number) { return this.products.filter(p => p.category_id === catId); }
}