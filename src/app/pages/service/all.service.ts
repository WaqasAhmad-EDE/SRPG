import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AllService {

  report_fab_clicked = 0
  pro = ""
  constructor() { }

  set_clicked_fab(opt){
    this.report_fab_clicked = opt
  }
  get_clicked_fab(){
    return this.report_fab_clicked
  }
}
