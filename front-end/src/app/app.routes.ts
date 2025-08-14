import { Routes } from '@angular/router';

// components
import { HomeComponent } from './components/pages/home/home.component';
import { InscricaoComponent } from './components/pages/inscricao/inscricao.component';
import { InscritoComponent } from './components/pages/inscrito/inscrito.component';
import { DependentesComponent } from './components/pages/dependentes/dependentes.component';
import { RecepcaoComponent } from './components/pages/recepcao/recepcao.component';
import { inscritoGuard } from './guard/inscrito/inscrito.guard';
import { dependenteGuard } from './guard/dependente/dependente.guard';
import { EsperaComponent } from './components/pages/espera/espera.component';
import { EsperaGuard } from './guard/espera/espera.guard';

export const routes: Routes = [
    //{path: 'home', component: HomeComponent, title: "Home | Musical ICCF"},
    {path: '', component: InscricaoComponent, title: "Inscrição | Musical ICCF"},
    {path: 'inscrito', component: InscritoComponent, canActivate: [inscritoGuard], title: "Inscrito | Musical ICCF"},
    {path: 'dependente', component: DependentesComponent, canActivate: [dependenteGuard], title: "dependentes | Musical ICCF"},
    {path: 'recepcao', component: RecepcaoComponent, title: "recepção | Musical ICCF"},
    {path: 'espera', component: EsperaComponent, canActivate: [EsperaGuard], title: "espera | Musical ICCF"},
    {path: '**', redirectTo: '', pathMatch: "full"}
];
