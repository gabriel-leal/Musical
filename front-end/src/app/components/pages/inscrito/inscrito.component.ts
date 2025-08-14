import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
import { isPlatformBrowser, NgFor } from '@angular/common';
import { InscritoService } from '../../../services/inscrito/inscrito.service';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-inscrito',
  standalone: true,
  imports: [NgFor],
  templateUrl: './inscrito.component.html',
  styleUrl: './inscrito.component.scss'
})
export class InscritoComponent implements OnInit {

  public pessoas: Array<any> = [];

  constructor(@Inject(PLATFORM_ID) private platformId: Object, private _inscritoservice: InscritoService, private _router: Router){
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

  ngOnInit(): void {
      this.getPessoas()
  }

  getPessoas() {
    if (isPlatformBrowser(this.platformId)) {
      const id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID)
      this._inscritoservice.inscrito(id).subscribe({
        next: (res) => {
          this.pessoas = res.content
          if (this.pessoas.length === 0) {
            this.exit()
          }
        },
        error: (err) => {
          console.log(err)
        }
      })
    }
  }

  goToDependentes(){
    localStorage.removeItem(LOCAL_STORAGE_KEYS.NOME)
    const nomes = this.pessoas[0].nomecompleto.split(' ')
    let pai = nomes[0]

    if (nomes[1] && nomes[1].length < 3 && nomes[2]) {
      pai += ' ' + nomes[1] + ' ' + nomes[2]
    } else if (nomes[1]) {
      pai += ' ' + nomes[1]
    }
    localStorage.setItem(LOCAL_STORAGE_KEYS.NOME, pai)
    this._router.navigate(['dependente'])
  }

  exit() {
    localStorage.clear()
    this._router.navigate(['/'])
  }
}
