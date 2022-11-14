import { Component, OnInit } from '@angular/core';
import { App } from '@capacitor/app';
import { Platform, NavController, IonRouterOutlet } from '@ionic/angular';

@Component({
  selector: 'app-contactus',
  templateUrl: './contactus.page.html',
  styleUrls: ['./contactus.page.scss'],
})
export class ContactusPage implements OnInit {

  constructor(
    // backButton ->
    private platform: Platform,
    private navCtrl: NavController,
    private routerOutlet: IonRouterOutlet,
    // backButton <-
    ) {
    // backButton ->
    this.platform.backButton.subscribeWithPriority(10000000,() => {
      if (this.routerOutlet.canGoBack()) {
        this.navCtrl.back()
      }
      else{
        App.exitApp()
      }     
    })
    // backButton <-
  }
  ngOnInit() {
  }

}
