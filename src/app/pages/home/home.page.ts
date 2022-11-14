
import { Component, } from '@angular/core';
import { App } from '@capacitor/app';
import { AlertController, IonRouterOutlet, NavController, Platform, PopoverController } from '@ionic/angular';
import { PopoverPage } from './../popover/popover.page';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  constructor(
    public popoverController: PopoverController,
    private routerOutlet: IonRouterOutlet,
    private platform: Platform,
    private navCtrl: NavController,
    public alertController: AlertController,

  ) {
    // Camera.requestPermissions()

    this.platform.backButton.subscribeWithPriority(10000000,async () => {
      alertController.dismiss()
      if (this.routerOutlet.canGoBack()) {
        this.navCtrl.back()
      }
      else{
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

  async presentPopover(ev: any) {
    const popover = await this.popoverController.create({
      component: PopoverPage,
      cssClass: 'my-custom-class',
      translucent: true,
      event: ev
    });
    await popover.present();
  }

  // async fun(){
  //   console.log("dwa")
  //     const image = await Camera.getPhoto({
  //       quality: 90,
  //       allowEditing: true,
  //       resultType: CameraResultType.Uri,
  //       source: CameraSource.Camera
  //     });
  //     console.log(image)

  // image.webPath will contain a path that can be set as an image src.
  // You can access the original file using image.path, which can be
  // passed to the Filesystem API to read the raw data of the image,
  // if desired (or pass resultType: CameraResultType.Base64 to getPhoto)
  // var imageUrl = image.webPath;

  // Can be set to the src of an image now
  // imageElement.src = imageUrl;
  // }

}
