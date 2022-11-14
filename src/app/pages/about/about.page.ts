import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { App } from '@capacitor/app';
import { IonRouterOutlet, NavController, Platform } from '@ionic/angular';

@Component({
  selector: 'app-about',
  templateUrl: './about.page.html',
  styleUrls: ['./about.page.scss'],
})
export class AboutPage implements OnInit {

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
