import { Component } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-espera',
  standalone: true,
  imports: [],
  templateUrl: './espera.component.html',
  styleUrl: './espera.component.scss'
})
export class EsperaComponent {

  constructor(private _router: Router){
    this._router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const preloader = document.querySelector('.preloader');
        if (preloader) {
          setTimeout(() => {
            preloader.classList.add('hidden');
          }, 600);
        }
      }
    });
  }
}
