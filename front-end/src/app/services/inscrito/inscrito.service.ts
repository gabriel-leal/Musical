import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InscritoService {

  private api = environment.apiUrl

  constructor(private http: HttpClient) { }

  public inscrito(id: any): Observable<any> {
    return this.http.get(`${this.api}/inscricoes/${id}`)
  }
}
