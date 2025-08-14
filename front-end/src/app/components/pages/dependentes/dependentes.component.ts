import { Component, OnInit } from '@angular/core';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
import { FormGroup, ReactiveFormsModule, Validators, FormBuilder } from '@angular/forms';
import { NgxMaskDirective } from 'ngx-mask';
import { NavigationEnd, Router } from '@angular/router';
import { InscricaoService } from '../../../services/inscricao/inscricao.service';
import { AppSnackBarService } from '../../../services/AppSnackBarService';
import { NgIf } from '@angular/common';
import { pid } from 'node:process';

@Component({
  selector: 'app-dependentes',
  standalone: true,
  imports: [ReactiveFormsModule, NgxMaskDirective, NgIf],
  templateUrl: './dependentes.component.html',
  styleUrl: './dependentes.component.scss'
})
export class DependentesComponent implements OnInit {

  public form!: FormGroup
  public pai: any = ''
  loading = false;
  
  constructor(private _router:Router, private formBuilder: FormBuilder, private _inscricaoservice: InscricaoService, private _snackbar: AppSnackBarService){
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
    this.pai = localStorage.getItem(LOCAL_STORAGE_KEYS.NOME)
    this.form = this.formBuilder.group({
      nomeCompleto: ['', Validators.required],
      dataNas: ['', Validators.required],
      celular: [''],
      email: [''],
      membro: ['1', Validators.required]
    })
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
    const pai = localStorage.getItem(LOCAL_STORAGE_KEYS.ID)
    const dependente = {nome: this.form.value.nomeCompleto, datanas: this.todate(this.form.value.dataNas), telefone: this.form.value.celular, email: this.form.value.email, membro: this.form.value.membro, idpai: pai}

    if (this.form.valid) {
      this.loading = true;
      this._inscricaoservice.dependente(dependente).subscribe({
        next: (res) => {
          console.log(res)
          this._router.navigate(['inscrito'])
        },
        error: (err) => {
          console.log(err)
          this.loading = false;
          if (err.error.detail === "registration already exists in main registration") {
            this._snackbar.openSnackBar('Telefone/Email repetido! Deixe em branco ou informe outro', 'warning')
          }
          if (err.error.detail === "registration already exists") {
            this._snackbar.openSnackBar('Dependente já cadastrado', 'warning')
          }
        }
      })
    } else {
      console.log('Invalid Form')
    }
  }

  goback() {
    this._router.navigate(['inscrito'])
  }
}
