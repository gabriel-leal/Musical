import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class InscricaoService {

  private api = environment.apiUrl

  constructor(private http: HttpClient) { }

  public inscricao(inscricao: any): Observable<any> {
    return this.http.post(`${this.api}/inscricao`, inscricao)
  }

  public dependente(dependente: any): Observable<any> {
    return this.http.post(`${this.api}/dependente`, dependente)
  }

  public listapessoas(): Observable<any> {
    return this.http.get(`${this.api}/inscricoes`)
  }

    public getPresentes(): Observable<any> {
    return this.http.get(`${this.api}/presentes`)
  }

      public editapresenca(id: number): Observable<any> {
    return this.http.put(`${this.api}/presenca/${id}`, null)
  }

}
