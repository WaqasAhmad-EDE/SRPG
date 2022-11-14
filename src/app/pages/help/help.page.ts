import { Component, OnInit } from '@angular/core';
import { App } from '@capacitor/app';
import { AlertController, IonRouterOutlet, NavController, Platform, PopoverController } from '@ionic/angular';
import { PopoverPage } from '../popover/popover.page';
import { AllService } from '../service/all.service';
@Component({
  selector: 'app-help',
  templateUrl: './help.page.html',
  styleUrls: ['./help.page.scss'],
})
export class HelpPage implements OnInit {

  constructor(
    public popoverController: PopoverController,
    public alertController: AlertController,
    private routerOutlet: IonRouterOutlet,
    private platform: Platform,
    private navCtrl: NavController,
    private allser: AllService,


  ) {
    this.platform.backButton.subscribeWithPriority(10000000, async () => {
      alertController.dismiss()
      if (this.routerOutlet.canGoBack()) {
        this.navCtrl.back()
      }
      else {
        const alert = await this.alertController.create({
          cssClass: 'my-custom-class',
          header: 'Confirm!',
          message: 'Are you sure you want to exit!',
          buttons: [
            {
              text: 'Cancel',
              role: 'cancel',
              cssClass: 'secondary',
              id: 'cancel-button',
              handler: (blah) => {
                // console.log('Confirm Cancel: blah');
              }
            }, {
              text: 'Okay',
              id: 'confirm-button',
              handler: () => {
                // console.log('Confirm Okay');
                App.exitApp()
              }
            }
          ]
        });
        await alert.present();
      }
    })

  }

  ngOnInit() {
  }


  async presentPopover(ev: any) {
    const popover = await this.popoverController.create({
      component: PopoverPage,
      cssClass: 'my-custom-class',
      translucent: true,
      event: ev
    });
    await popover.present();


  }

  changepro(e :Event){
    this.allser.pro = e.target["value"]
    
  }

}
