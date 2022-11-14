import { Component, OnInit } from '@angular/core';
import { AlertController, Platform } from '@ionic/angular';
import { AllService } from '../service/all.service';

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.page.html',
  styleUrls: ['./tabs.page.scss'],
})
export class TabsPage {

  backdrop = false
  fab_activated = false
  constructor(
    private allServ: AllService,
    private platform: Platform,
    public alertController: AlertController,


  ) {



  }

  ngOnInit() {
    setTimeout(
      async () => {
        const myalert = await this.alertController.create({
          cssClass: 'my-custom-class',
          header: 'Note',
          message: 'This app is supposed to give result on fabric, results may fluctuate if any other image will be provided.',
          buttons: [
            {
              text: 'Okay',
              id: 'confirm-button',
            }
          ]
        });
        await myalert.present();
      },
      1500

    )
  }
  ionViewWillEnter() {
    this.backdrop = false
  }

  toggle_backdrop() {
    this.backdrop = !this.backdrop
  }


  clicked_fab(opt: any) {
    this.backdrop = false
    this.allServ.set_clicked_fab(opt)
  }

}
