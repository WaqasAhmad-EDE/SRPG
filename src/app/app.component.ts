import { AfterViewInit, Component } from '@angular/core';
// import { ScreenOrientation } from '@awesome-cordova-plugins/screen-orientation/ngx';
// import { SplashScreen } from "@capacitor/splash-screen"

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent implements AfterViewInit {
  check = false
  constructor(
  ) {

    // this.screenOrientation.lock('portrait')
    // SplashScreen.hide()
  }
  ngAfterViewInit() {
    // setTimeout(() => {
    //   this.check = !this.check
    //   // }, 0);
    // }, 3200);
  }
}
