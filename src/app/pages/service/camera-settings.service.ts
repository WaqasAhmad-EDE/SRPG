import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CameraSettingsService {

  camera_flash = true
  camera_zoom = 50 
  camera_position = 2
  camera_size = 200
  constructor() {
    this.camera_zoom = 100 
    this.camera_flash = true
    this.camera_position = 2
    this.camera_size = 200
   }

}
