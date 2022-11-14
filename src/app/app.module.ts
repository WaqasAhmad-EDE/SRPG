import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';


import { HttpClientModule } from '@angular/common/http';

import { CameraPreview} from '@awesome-cordova-plugins/camera-preview/ngx';
// import { ScreenOrientation } from '@awesome-cordova-plugins/screen-orientation/ngx';

import { PhotoViewer } from '@awesome-cordova-plugins/photo-viewer/ngx';

@NgModule({
  declarations: [AppComponent],
  entryComponents: [],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule,HttpClientModule ],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy },CameraPreview,PhotoViewer],
  bootstrap: [AppComponent],
})
export class AppModule {}
