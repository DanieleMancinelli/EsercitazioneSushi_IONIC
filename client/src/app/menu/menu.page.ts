import { Component, OnInit } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { SushiService } from '../services/sushi';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.page.html',
  styleUrls: ['./menu.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule]
})
export class MenuPage implements OnInit {
  products: any[] = [];
  categories: any[] = [];

  constructor(private sushiService: SushiService) {}

  ngOnInit() {
    this.sushiService.getMenu().subscribe(data => {
      this.products = data.products;
      this.categories = data.categories;
    });
  }

  // Filtra i prodotti per categoria
  getProductsByCategory(catId: number) {
    return this.products.filter(p => p.category_id === catId);
  }
}