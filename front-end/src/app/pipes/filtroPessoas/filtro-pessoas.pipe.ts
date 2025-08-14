import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filtroPessoas',
  standalone: true // use isso se estiver com component standalone
})
export class FiltroPessoasPipe implements PipeTransform {
  transform(pessoas: any[], termo: string): any[] {
    if (!pessoas) return [];
    if (!termo) return pessoas;

    termo = termo.toLowerCase();

    return pessoas.filter(pessoa =>
      pessoa.nomecompleto.toLowerCase().includes(termo)
    );
  }
}