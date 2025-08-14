import { Component, OnInit, Inject } from '@angular/core';
import { MatSnackBarRef, MAT_SNACK_BAR_DATA } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-snackbar',
  standalone: true,
  imports: [MatIconModule, NgClass],
  templateUrl: './app-snackbar.component.html',
  styleUrls: ['./app-snackbar.component.scss']
})
export class AppSnackbarComponent implements OnInit {

  snackType: string = '';

  constructor(
    @Inject(MAT_SNACK_BAR_DATA) 
    public data: any,
    private _snackRef: MatSnackBarRef<AppSnackbarComponent>,
    ) {
    this.snackType = this.data.snackType;
  }

  ngOnInit() { 
  }

  get getIcon() {
    switch (this.snackType) {
      case 'success':
        return 'check_circle';
      case 'error':
        return 'cancel';
      case 'warn':
        return 'warning';
      case 'info':
        return 'error';
      default: return this.data.snackType;
    }
  }

  public dismiss(){
    this._snackRef.dismiss();
  }
}
