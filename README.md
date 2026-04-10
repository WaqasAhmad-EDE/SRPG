# Automatic Reed Pick Glass (SRPG)

## Overview

This repository contains an Ionic + Angular mobile application called **Automatic Reed Pick Glass**. The app is built to help textile and quality control teams inspect fabric properties using a smartphone camera. It uses live camera preview to capture fabric images and then sends those images to a remote analysis service for automated fabric quality evaluation.

The app is intended for use on Capacitor-enabled mobile devices and includes a simplified workflow for selecting a fabric test, capturing an image, and viewing results. It is especially focused on the practical inspection of woven fabric characteristics like color consistency, dimensional stability, and fabric dimensions.

## Live Testing

A hosted live demo is available at: <a href="https://srpg-4cd35.web.app/tabs/home" target="_blank" rel="noopener noreferrer">https://srpg-4cd35.web.app/tabs/home</a>


## What the Project Does

- Provides a mobile interface for fabric quality inspection.
- Lets users choose specific fabric tests from a floating action button menu.
- Opens a live camera preview so the user can capture the fabric under inspection.
- Submits the captured image to a remote analysis endpoint and returns quality metrics.
- Displays results in expandable cards with original and processed image previews.
- Includes a help section with instructions for each test type.
- Offers configuration for camera settings such as flash, zoom, capture size, and position.

## Detailed Features

- **Home and Quick Access**
  - Central home page with a popover menu for navigation.
  - A floating action button menu with four analysis options:
    - Color Consistency
    - Fabric Dimensions
    - Dimensional Stability
    - Overall Quality
- **Report Workflow**
  - Each option leads to the `Report` page for image capture and analysis.
  - The camera preview starts on demand and supports rear-camera capture.
  - Capture, accept, reset, and close camera controls are provided.
  - After accepting a photo, the app sends the image as Base64 to a remote API.
- **Result Display**
  - Results are shown in expandable cards.
  - Some cards display an image preview of the original capture and a processed image if available.
  - Loading spinners show network progress while analysis is running.
- **Settings**
  - Toggle flash on/off.
  - Select camera zoom level.
  - Choose capture area size.
  - Position the camera preview area on the screen.
- **Help and Support**
  - Help page explains how to use the app for each fabric test.
  - Contact page includes team member contact details.
  - About page shows app branding and version information.

## Architecture

- `src/app/app.module.ts` - Root module imports `IonicModule`, `AppRoutingModule`, `HttpClientModule`, and Cordova plugin providers.
- `src/app/app-routing.module.ts` - Main public routes for the app.
- `src/app/pages/tabs` - Tabbed container that wraps `home` and `help` pages.
- `src/app/pages/report/report.page.ts` - Core page for camera capture, image submission, and result display.
- `src/app/pages/setting/setting.page.ts` - Page for managing camera preferences.
- `src/app/pages/help/help.page.ts` - Usage guide and FAQ content.
- `src/app/pages/popover/popover.page.ts` - Floating menu navigation.
- `src/app/pages/contactus` and `src/app/pages/about` - Informational pages.
- `src/app/pages/service` - Shared services used for app state and camera settings.

## Notable Dependencies

- `@ionic/angular` - Ionic UI component library.
- `@angular/core`, `@angular/router`, `@angular/common/http` - Angular framework modules.
- `@capacitor/core`, `@capacitor/app`, `@capacitor/filesystem` - Capacitor runtime and native functionality.
- `@awesome-cordova-plugins/camera-preview` - Live camera preview and capture.
- `@awesome-cordova-plugins/photo-viewer` - Fullscreen image viewer for result previews.

## Important Files

- `package.json` - Project dependencies and scripts.
- `angular.json` - Angular CLI configuration.
- `capacitor.config.ts` - Capacitor settings and native integration.
- `src/app/pages/report/report.page.ts` - Main feature implementation for image capture and quality analysis.
- `src/app/pages/setting/setting.page.ts` - Camera configuration options.
- `src/app/pages/help/help.page.html` - Help content and workflow instructions.
- `main.py`, `process.py` - Python files at the repository root, likely part of backend or additional processing support outside the Ionic app.

## Installation

From the repository root:

```bash
npm install
```

## Run locally

For development in a browser:

```bash
npm start
```

This starts the Angular dev server via `ng serve`.

## Build

To build the app for production:

```bash
npm run build
```

## Android / Capacitor

If you want to deploy to Android, use Capacitor commands after building:

```bash
npm run build
npx cap sync android
npx cap open android
```

> Note: The `CameraPreview` plugin and Capacitor native functionality work best on a physical device or emulator, not in a standard browser.

## Usage Notes

- The app sends image data to `https://srpg.pythonanywhere.com/quality` for fabric analysis.
- The `Report` page supports multiple tests through a shared remote endpoint.
- Camera settings are managed by `CameraSettingsService` and persist while the app runs.
- The app assumes a Capacitor-enabled mobile environment for native camera and filesystem behavior.

## Recommendations

- Use a physical Android device or emulator for full camera support.
- Confirm the remote API endpoint is available before testing the report flow.
- Consider updating dependencies if you need compatibility with newer Ionic/Angular releases.
