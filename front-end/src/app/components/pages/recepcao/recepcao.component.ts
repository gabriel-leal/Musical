import { NgFor, NgIf, NgStyle } from '@angular/common';
import { Component, OnInit, ViewChild } from '@angular/core';
import { NgxScannerQrcodeComponent, ScannerQRCodeConfig } from 'ngx-scanner-qrcode';
import { InscricaoService } from '../../../services/inscricao/inscricao.service';
import { AppSnackBarService } from '../../../services/AppSnackBarService';
import { FormsModule } from '@angular/forms';
import { FiltroPessoasPipe } from '../../../pipes/filtroPessoas/filtro-pessoas.pipe';
import { LOCAL_STORAGE_KEYS } from '../../../app.config';
declare var bootstrap: any;

@Component({
  selector: 'app-recepcao',
  standalone: true,
  imports: [NgxScannerQrcodeComponent, NgIf, NgFor, NgStyle, FormsModule, FiltroPessoasPipe],
  templateUrl: './recepcao.component.html',
  styleUrl: './recepcao.component.scss'
})
export class RecepcaoComponent implements OnInit {

  constructor(private _inscricaoservice: InscricaoService, private _snackbar: AppSnackBarService){}

  @ViewChild('action') action!: NgxScannerQrcodeComponent;

  scannedValue: any;
  id: any;
  pessoas: any[] = []
  pessoaSelecionada: any = {};
  filtro: string = '';
  

  total = 0
  presentes = 0

  config: ScannerQRCodeConfig = {
    constraints: {
    video: {
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
    },
    isBeep: true,
    vibrate: 300,
  };

  ngOnInit(): void {
      this.getPessoas()
      this.totalPresenca()
  }

  abrirModal() {
  const modalElement = document.getElementById('verticalycentered');
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  }
}

  scanSuccess(event: any): void {
    //console.log('🟢 scanSuccess chamado com:', event);
    this.scannedValue = event;
    if (Array.isArray(this.scannedValue)) {
      this.action?.stop()
      this.scannedValue.forEach((element: any) => {
      this.id = element.value
      this.presente()

      });
    } else {
      console.log('scannedValue is not an array');
    }
  }

  public alteraPresenca(pessoa: any) {
    this.pessoaSelecionada = pessoa
    if (this.pessoaSelecionada.presenca == 0) {
      this._inscricaoservice.editapresenca(this.pessoaSelecionada.id).subscribe({
        next: (res) => {
          this.getPessoas()
          this.filtro = '';
          setTimeout(() => {
            const el = document.getElementById(this.pessoaSelecionada.id.toString());
            if (el) {
              el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          }, 100);
        },
        error: (err) => {
          console.log(err)
        }
      })
    } else {
      console.log('pessoa já presente')
      this.abrirModal()
      this.filtro = '';
    }
  }

  cancelaPresenca(){
  this._inscricaoservice.editapresenca(this.pessoaSelecionada.id).subscribe({
      next: (res) => {
        this.getPessoas()
      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  public getPessoas() {
    const adm = localStorage.getItem(LOCAL_STORAGE_KEYS.ADM)
    if (adm === '1') {
      this._inscricaoservice.listapessoas().subscribe({
        next: (res) => {
          this.pessoas = [];
          this.pessoas.push(res.content)
          this.pessoas = this.pessoas.flat()
          this.total = this.pessoas.length
          this.totalPresenca()
        },
        error: (err) => {
          console.log(err)
        }
      })
    }
  }

  public presente() {
    const id = Number(this.id)
    this.pessoaSelecionada = this.pessoas.find(p => p.id === id);
    if (this.pessoaSelecionada.presenca === 0) {
      this._inscricaoservice.editapresenca(id).subscribe({
        next: (res) => {
          console.log(res)
          this.getPessoas()
           setTimeout(() => {
            const el = document.getElementById(this.pessoaSelecionada.id.toString());
            if (el) {
              el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          }, 100);
        },
        error: (err) => {
          console.log(err)
        }
      })
    } else {
      this._snackbar.openSnackBar('Esse QRcode Já Foi Lido!', 'warning')
    }
  }

  public totalPresenca() {
    this._inscricaoservice.getPresentes().subscribe({
      next: (res) => {
        this.presentes = res.totalpresenca
      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  activaRecepcao(text: string){
    const adm = localStorage.getItem(LOCAL_STORAGE_KEYS.ADM)
    if (adm === null) {
      if (text === 'ADM') {
        localStorage.setItem(LOCAL_STORAGE_KEYS.ADM, '1')
        location.reload();
      }
    }
  }
}
