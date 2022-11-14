import { Component, OnInit } from '@angular/core';
import { App } from '@capacitor/app';
import { Platform, NavController, IonRouterOutlet } from '@ionic/angular';
import { CameraSettingsService } from '../service/camera-settings.service';

@Component({
  selector: 'app-setting',
  templateUrl: './setting.page.html',
  styleUrls: ['./setting.page.scss'],
})
export class SettingPage implements OnInit {

  camera_zoom: number
  camera_flash: boolean
  camera_position: number
  camera_size: number
  w: number

  constructor(

    public cameraSetting: CameraSettingsService,
    // backButton ->
    private platform: Platform,
    private navCtrl: NavController,
    private routerOutlet: IonRouterOutlet,
    // backButton <-
  ) {
    // backButton ->
    this.platform.backButton.subscribeWithPriority(10000000, () => {
      if (this.routerOutlet.canGoBack()) {
        this.navCtrl.back()
      }
      else {
        App.exitApp()
      }
    })
    // backButton <-
    this.camera_zoom = this.cameraSetting.camera_zoom
    this.camera_flash = this.cameraSetting.camera_flash
    this.camera_position = this.cameraSetting.camera_position
    this.camera_size = this.cameraSetting.camera_size
    this.w = window.screen.width
  }
  ngOnInit() {
  }

  set_zoom(zoom: number) {
    this.cameraSetting.camera_zoom = zoom
  }

  set_flash() {
    this.camera_flash = !this.camera_flash
    this.cameraSetting.camera_flash = !this.cameraSetting.camera_flash
  }

  set_size(ev: Event) {
    this.cameraSetting.camera_size = Number(ev['detail'].value)
  }

  set_position(ev: Event) {
    this.cameraSetting.camera_position = Number(ev['detail'].value)
  }

}
