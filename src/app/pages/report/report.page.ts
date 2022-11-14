import { Component, OnInit } from '@angular/core';
import { AllService } from '../service/all.service';
import { App } from '@capacitor/app';
import { Platform, NavController, IonRouterOutlet } from '@ionic/angular';
import { HttpClient } from '@angular/common/http';

import { CameraPreview, CameraPreviewPictureOptions, CameraPreviewOptions, CameraPreviewDimensions } from '@awesome-cordova-plugins/camera-preview/ngx';
import { Filesystem, Directory, Encoding, WriteFileOptions, ReadFileOptions, ReaddirOptions } from '@capacitor/filesystem';

import { AlertController } from '@ionic/angular';
import { CameraSettingsService } from '../service/camera-settings.service';
import { PhotoViewer } from '@awesome-cordova-plugins/photo-viewer/ngx';

@Component({
  selector: 'app-report',
  templateUrl: './report.page.html',
  styleUrls: ['./report.page.scss'],
})
export class ReportPage {

  card_to_show = 0
  all_expanded = false
  disable_cards = true
  camera_button_status = [true, false, false, false, false]
  full_card = [false, false, false, false, false];
  picture: any;
  captured = false
  FDImage: any

  SPDS = true
  SPCC = true
  SPFD = true
  PRDS = false
  PRCC = false
  PRFD = false

  CC = 0
  DS = 0
  FD = 0


  url = ""

  constructor(
    private allServ: AllService,
    public alertController: AlertController,
    private cameraPreview: CameraPreview,
    private cameraSettings: CameraSettingsService,
    private httpclient: HttpClient,
    private photoviewer: PhotoViewer,

    // backButton ->
    private platform: Platform,
    private navCtrl: NavController,
    private routerOutlet: IonRouterOutlet,
    // backButton <-
  ) {
    // this.url = "http://" + this.allServ.pro+":5000/quality"
    this.url = "https://srpg.pythonanywhere.com/quality"
    Filesystem.requestPermissions()
    this.card_to_show = allServ.get_clicked_fab()
    // backButton ->
    this.platform.backButton.subscribeWithPriority(10000000, async () => {
      alertController.dismiss()
      if (this.routerOutlet.canGoBack()) {
        if (!this.disable_cards) {
          // alert("Are you sure you want to stop!")
          const alert = await this.alertController.create({
            cssClass: 'my-custom-class',
            header: 'Confirm!',
            message: 'Process will be stoped!',
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
                  this.navCtrl.back()
                }
              }
            ]
          });
          await alert.present();
        }
        else {
          this.navCtrl.back()
        }
      }
      else {
        App.exitApp()
      }
    })
    // backButton <-
  }


  ngOnInit() {
  }
  ngOnDestroy() {
    this.cameraPreview.stopCamera()
  }
  expand_contract() {
    for (let index = 0; index < 5; index++) {
      this.full_card[index] = !this.all_expanded
    }
    this.all_expanded = !this.all_expanded
  }

  expandimage(img) {
    this.photoviewer.show(img)
  }

  toggle_card(i: number) {

    this.full_card[i] = !this.full_card[i]
    for (let index = 0; index < 5; index++) {
      if (this.full_card[index] == true) {
        this.all_expanded = true
        return
      }
    }
    this.all_expanded = false
  }

  async open_camera() {

    if(
      this.SPDS == false ||
      this.SPCC == false ||
      this.SPFD == false
      )
      {
        return
      }

    this.camera_button_status[0] = false
    this.camera_button_status[1] = true
    this.camera_button_status[4] = true

    let w = window.screen.width;
    let h = window.screen.height;


    // let options: CameraPreviewOptions 
    // = {
    //   camera: "rear",
    //   storeToFile: false
    // }
    // options.x = (w / 2) - (this.cameraSettings.camera_size / 2)
    // options.y = (h / this.cameraSettings.camera_position) - (this.cameraSettings.camera_size / 2)
    // options.width = this.cameraSettings.camera_size
    // options.height = this.cameraSettings.camera_size
    // options.camera = 'rear'
    // options.storeToFile = false

    let options: CameraPreviewOptions = {
      // x: (w / 2) - (this.cameraSettings.camera_size / 2),
      // y: (h / this.cameraSettings.camera_position) - (this.cameraSettings.camera_size / 2),
      // width: this.cameraSettings.camera_size,
      // height: this.cameraSettings.camera_size,
      height: h * 0.80,
      camera: "rear",
      storeToFile: false,
    };

    await this.cameraPreview.startCamera(options);
    if (this.cameraSettings.camera_flash) {
      await this.cameraPreview.setFlashMode(this.cameraPreview.FLASH_MODE.TORCH)
    }



    await this.cameraPreview.getMaxZoom().then((maxZoom) => {
      this.cameraPreview.setZoom(maxZoom * this.cameraSettings.camera_zoom / 100)
    })



  }



  async close_camera() {
    // this.picture = ''
    this.camera_button_status = [true, false, false, false, false]
    this.captured = false
    await this.cameraPreview.stopCamera();
  }



  reset_image() {
    this.camera_button_status[2] = false
    this.camera_button_status[3] = false
    this.camera_button_status[4] = true

    this.picture = ''
    this.captured = false
    this.open_camera()
  }


  async accept_image() {


    this.disable_cards = false

    this.close_camera()


    if (this.allServ.get_clicked_fab() == 4) {
    }
    
    // ye fab sy sai karna
    
    if (this.allServ.get_clicked_fab() == 1 || this.allServ.get_clicked_fab() == 4) {
      this.SPCC = false
      this.PRCC = false
      this.httpclient
      .post(this.url, { image: this.picture, fab: 1 })
      .subscribe(res => {
        this.SPCC = true
        this.PRCC = true
        this.CC = parseInt(JSON.stringify(res))
      })
      // return
    }
    
    if (this.allServ.get_clicked_fab() == 2 || this.allServ.get_clicked_fab() == 4) {
      this.SPFD = false
      this.PRFD = false
      this.httpclient
      .post(this.url, { image: this.picture, fab:2 })
      .subscribe(res => {
        this.SPFD = true
        this.PRFD = true
        this.FDImage = res
      })
      // return
    }
    
    if (this.allServ.get_clicked_fab() == 3 || this.allServ.get_clicked_fab() == 4) {
      this.SPDS = false
      this.PRDS = false
      this.httpclient
        .post(this.url, { image: this.picture, fab: 3 })
        .subscribe(res => {
          this.SPDS = true
          this.PRDS = true
          this.DS = parseInt(JSON.stringify(res))
        })
      // return
    }
    // if (this.allServ.get_clicked_fab() == 4) {
    //   this.httpclient
    //     .post(this.url , { image: this.picture, fab: this.allServ.get_clicked_fab() })
    //     .subscribe(res => {
    //     })
    //   return
    // }





    // this.httpclient
    //   .post(this.url , { image: this.picture, fab: this.allServ.get_clicked_fab() })
    //   .subscribe(res => {


    //     if (this.allServ.get_clicked_fab() == 1) {
    //     }

    //     if (this.allServ.get_clicked_fab() == 3) {
    //     }
    //   })




    // let image = this.picture
    // const fileName = new Date().getTime() + '.jpeg';
    // var optionWrite: WriteFileOptions = {
    //   path: "AutomaticReedPickGlass/" + fileName,
    //   directory: Directory.ExternalStorage,
    //   recursive: true,
    //   data: image,
    // }
    // await Filesystem.writeFile(optionWrite).then((results) => {

    //   // req server


    //   console.log(this.picture)
    // }, (error) => {
    // }
    // )


    // var optionWriteStatus: WriteFileOptions = {
    //   path: "AutomaticReedPickGlass/Status.txt",
    //   directory: Directory.ExternalStorage,
    //   recursive: true,
    //   encoding: Encoding.UTF8,
    //   data: fileName,
    // }
    // await Filesystem.writeFile(optionWriteStatus).then((results) => {
    // }, (error) => {
    // }
    // )
    // this.disable_cards = false
    // setTimeout(() => {
    // }, 3000);
  }


  async take_photo() {

    const pictureOpts: CameraPreviewPictureOptions = {
      quality: 100,
    }

    await this.cameraPreview.takePicture(pictureOpts).then(async (imageData) => {
      this.picture = 'data:image/jpeg;base64,' + imageData
      await this.cameraPreview.stopCamera()
      this.captured = true
    }, (err) => {
      // alert(err);
    })



    this.camera_button_status[2] = true
    this.camera_button_status[3] = true
    this.camera_button_status[4] = false

  }



  // async open_camera() {
  //   const image = await Camera.getPhoto({
  //     quality: 90,
  //     // allowEditing: true,
  //     resultType: CameraResultType.Uri,
  //     source: CameraSource.Camera
  //   });



  //   // console.log(image)

  //   // image.webPath will contain a path that can be set as an image src.
  //   // You can access the original file using image.path, which can be
  //   // passed to the Filesystem API to read the raw data of the image,
  //   // if desired (or pass resultType: CameraResultType.Base64 to getPhoto)
  //   // var imageUrl = image.webPath;

  //   // Can be set to the src of an image now
  //   // imageElement.src = imageUrl;
  // }

  // async open_gallary() {
  //   const image = await Camera.getPhoto({
  //     quality: 90,
  //     allowEditing: true,
  //     resultType: CameraResultType.Uri,
  //     source: CameraSource.Photos
  //   });
  //   console.log(image)

  //   // image.webPath will contain a path that can be set as an image src.
  //   // You can access the original file using image.path, which can be
  //   // passed to the Filesystem API to read the raw data of the image,
  //   // if desired (or pass resultType: CameraResultType.Base64 to getPhoto)
  //   // var imageUrl = image.webPath;

  //   // Can be set to the src of an image now
  //   // imageElement.src = imageUrl;

  // }

}
