import { Component } from '@angular/core';
import { IonicModule, NavController } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true,
  imports: [IonicModule, FormsModule, CommonModule],
})
export class HomePage {
  tableNumber: string = '';
  userName: string = '';

  constructor(private navCtrl: NavController) {}

  login() {
    if (this.tableNumber && this.userName) {
      // Salviamo i dati nel browser per ricordarli durante l'ordine
      localStorage.setItem('table', this.tableNumber);
      localStorage.setItem('user', this.userName);
      this.navCtrl.navigateForward('/menu');
    }
  }
}