import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppSnackbarComponent } from '../components/app-snackbar/app-snackbar.component';
 
@Injectable({
  providedIn: 'root'
})
export class AppSnackBarService {
  constructor(private snackBar: MatSnackBar) {}
  public openSnackBar(message: string, snackType: string) {

    this.snackBar.openFromComponent(AppSnackbarComponent, {
      duration: 5000,
      panelClass: [snackType, 'custom-snackbar'],
      data: { message: message, snackType: snackType },
      politeness: 'assertive'
    });
  }
}
