import { CommonModule } from '@angular/common';
import { Component, HostListener, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  windowWidth: number = 0;

  constructor(@Inject(PLATFORM_ID) private platformId: Object, private _router: Router) {
        this._router.events.subscribe(event => {
          if (event instanceof NavigationEnd) {
            const preloader = document.querySelector('.preloader');
            if (preloader) {
              setTimeout(() => {
                preloader.classList.add('hidden');
              }, 1000);
              
            }
          }
        });
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any) {
    if (isPlatformBrowser(this.platformId)) {
      this.windowWidth = window.innerWidth;
    }
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.windowWidth = window.innerWidth;
    }
  }
}