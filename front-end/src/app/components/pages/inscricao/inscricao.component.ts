import { isPlatformBrowser, NgClass, NgIf } from '@angular/common';
import { Component, Inject, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NgxMaskDirective } from 'ngx-mask';
import { InscricaoService } from '../../../services/inscricao/inscricao.service';
import { NavigationEnd, Router } from '@angular/router';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
import { AppSnackBarService } from '../../../services/AppSnackBarService';
import { EsperaAccessService } from '../../../services/espera/espera.service';

@Component({
  selector: 'app-inscricao',
  standalone: true,
  imports: [NgIf, NgClass, NgxMaskDirective, ReactiveFormsModule],
  templateUrl: './inscricao.component.html',
  styleUrl: './inscricao.component.scss'
})
export class InscricaoComponent implements OnInit {

  mostrarModal = false;
  public form!: FormGroup
  loading = false;
  total: number = 0
  

  constructor(private formBuilder: FormBuilder, private _inscricaoservice: InscricaoService, private esperaAccess: EsperaAccessService, private _router: Router, @Inject(PLATFORM_ID) private platformId: Object, private _snackbar: AppSnackBarService){
    if (isPlatformBrowser(platformId)) {
    const id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID);
    if (id !== null && !isNaN(Number(id))) {
      this._router.navigate(['inscrito']);
    } else {
      this.confereQtd()
    }
    }
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
    this.form = this.formBuilder.group({
      nomeCompleto: ['', Validators.required],
      dataNas: ['', Validators.required],
      celular: ['', Validators.required],
      email: ['', Validators.email],
      membro: ['1', Validators.required],
      checkbox: ['', Validators.required]
    })
  }

  confereIncricao() {
    if (isPlatformBrowser(this.platformId)) {
      const id = localStorage.getItem(LOCAL_STORAGE_KEYS.ID)
      if (id !== null && !isNaN(Number(id))) {
        this._router.navigate(['inscrito']);
      }
    }
  }

  confereQtd() {
    this._inscricaoservice.listapessoas().subscribe({
      next: (res) => {
        this.total = res.size
        if (this.total >= 71) {
          this.goToEspera()
        }
      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  goToEspera() {
    this.esperaAccess.permitAccess();
    this._router.navigate(['/espera']);
  }

  todate(string: string){
    const str = string;
    const day = str.substring(0, 2);
    const month = str.substring(2, 4);
    const year = str.substring(4, 8);

    const formattedDate = `${year}-${month}-${day}`;
    return formattedDate
  }

  submit() {
  const inscricao = {
    nome: this.form.value.nomeCompleto,
    datanas: this.todate(this.form.value.dataNas),
    telefone: this.form.value.celular,
    email: this.form.value.email,
    membro: this.form.value.membro
  };

  if (this.form.valid) {
    this.loading = true;

    this._inscricaoservice.inscricao(inscricao).subscribe({
      next: (res) => {
        localStorage.setItem(LOCAL_STORAGE_KEYS.ID, res.id);
        this._router.navigate(['inscrito']);
      },
      error: (err) => {
        console.log(err);

        if (err.error.detail?.message === 'login in registration') {
          localStorage.setItem(LOCAL_STORAGE_KEYS.ID, err.error.detail?.value);
          console.log('passou')
          this._router.navigate(['inscrito']);
        } else {
          this.loading = false;
        }
        if (err.error.detail === "registration already exists in dependents") {
          this._snackbar.openSnackBar('Inscrição já realizada como dependente', 'warning')
        }
        if (err.error.detail === "registration already exists") {
          this._snackbar.openSnackBar('Dados errados', 'warning')
        }
      }
    });
    } else {
      console.log('Invalid Form');
      this.loading = false;
    }
  }
}
